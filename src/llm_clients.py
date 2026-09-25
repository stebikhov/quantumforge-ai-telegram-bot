"""LLM-клиенты для RAG-пайплайна.

Поддерживается переключение провайдера через переменную окружения LLM_PROVIDER:
- "yandex" (по умолчанию, если задан YANDEX_GPT_API_KEY) — YandexGPT через yandex-cloud-ml-sdk
- "openai"   — OpenAI-совместимый API (OpenAI, LM Studio, Ollama и т.п.)
- "ollama"   — Явная поддержка Ollama с оптимизированными настройками
- "stub"     — заглушка без реального вызова LLM (для офлайн-демонстрации)

Каждый клиент реализует единый интерфейс:
    generate(prompt: str, *, system: str | None = None) -> str
"""
from __future__ import annotations

import logging
import os
import random
import time
from typing import Optional, Protocol
from config import DEMO_MODE, DEMO_RESPONSES, DEFAULT_LLM_PROVIDER, DEFAULT_LLM_MODEL, OLLAMA_BASE_URL, OLLAMA_DEFAULT_MODEL

logger = logging.getLogger(__name__)


class LLMClient(Protocol):
    """Протокол для LLM-клиентов."""
    
    def generate(self, prompt: str, *, system: Optional[str] = None) -> str:
        """Генерирует ответ на основе промпта.
        
        Args:
            prompt: Пользовательский промпт с контекстом
            system: Системный промпт (опционально)
            
        Returns:
            Сгенерированный текст ответа
        """
        ...


class StubLLMClient:
    """Заглушка: возвращает демонстрационные ответы или уведомление."""

    def __init__(self, demo_mode: bool = False):
        """Инициализация заглушки.
        
        Args:
            demo_mode: Если True, возвращает реалистичные демо-ответы
        """
        self.demo_mode = demo_mode

    def generate(self, prompt: str, *, system: Optional[str] = None) -> str:
        """Генерирует демонстрационный ответ.
        
        В демо-режиме возвращает реалистичные ответы, иначе - уведомление.
        """
        if self.demo_mode:
            # Выбираем случайный демо-ответ
            demo_response = random.choice(DEMO_RESPONSES)
            return f"{demo_response}\n\n[Демо-режим: для реальных ответов настройте API-ключи]"
        else:
            return (
                "LLM не подключена. Для полноценных ответов настройте LLM_PROVIDER "
                "и соответствующие API-ключи в .env (см. README)."
            )


class YandexGPTClient:
    """Клиент YandexGPT через yandex-cloud-ml-sdk.

    Требует:
        YANDEX_GPT_API_KEY  — API-ключ сервисного аккаунта
        YANDEX_GPT_FOLDER_ID — идентификатор каталога
    Опционально:
        LLM_MODEL — имя модели (по умолчанию yandexgpt-lite)
        LLM_TEMPERATURE
        LLM_MAX_TOKENS
    """

    DEFAULT_MODEL = "yandexgpt-lite"

    def __init__(
        self,
        api_key: Optional[str] = None,
        folder_id: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ):
        """Инициализация клиента YandexGPT.
        
        Args:
            api_key: API-ключ Yandex Cloud
            folder_id: ID каталога Yandex Cloud
            model: Имя модели YandexGPT
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов в ответе
        """
        self.api_key = api_key or os.getenv("YANDEX_GPT_API_KEY")
        self.folder_id = folder_id or os.getenv("YANDEX_GPT_FOLDER_ID")
        self.model = model or os.getenv("LLM_MODEL", self.DEFAULT_MODEL)
        self.temperature = float(os.getenv("LLM_TEMPERATURE", temperature))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", max_tokens))

        if not self.api_key:
            raise RuntimeError(
                "YANDEX_GPT_API_KEY не задан. Укажите ключ в .env "
                "(см. README → Настройка LLM)."
            )
        if not self.folder_id:
            raise RuntimeError(
                "YANDEX_GPT_FOLDER_ID не задан. Укажите folder_id каталога в .env."
            )

        try:
            from yandex_cloud_ml_sdk import YCloudML  # type: ignore
        except ImportError as e:
            raise RuntimeError(
                "Пакет yandex-cloud-ml-sdk не установлен. "
                "Выполните: pip install -r requirements.txt"
            ) from e

        self._sdk = YCloudML(folder_id=self.folder_id, auth=self.api_key)
        self._model = self._sdk.models.completions(self.model).configure(
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        logger.info(
            "YandexGPTClient инициализирован: model=%s, folder=%s",
            self.model,
            self.folder_id,
        )

    def generate(self, prompt: str, *, system: Optional[str] = None) -> str:
        """Генерирует ответ с помощью YandexGPT.
        
        Args:
            prompt: Пользовательский промпт с контекстом
            system: Системный промпт (опционально)
            
        Returns:
            Сгенерированный текст ответа
        """
        messages = []
        if system:
            messages.append({"role": "system", "text": system})
        messages.append({"role": "user", "text": prompt})

        result = self._model.run(messages)
        try:
            return result.alternatives[0].text
        except (AttributeError, IndexError) as e:
            logger.error("Ошибка парсинга ответа YandexGPT: %s", e)
            return "Ошибка при генерации ответа YandexGPT."


class OpenAILLMClient:
    """Клиент OpenAI-совместимого API.

    Поддерживает:
        - Официальный OpenAI API
        - LM Studio (localhost:1234/v1)
        - Ollama (http://localhost:11434/v1)
        - Любой другой OpenAI-совместимый эндпоинт

    Требует:
        OPENAI_API_KEY — API-ключ
    Опционально:
        OPENAI_BASE_URL — базовый URL (по умолчанию https://api.openai.com/v1)
        LLM_MODEL       — имя модели (по умолчанию gpt-4o-mini)
        LLM_TEMPERATURE
        LLM_MAX_TOKENS
    """

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 800,
        timeout: int = 60,
    ):
        """Инициализация клиента OpenAI.
        
        Args:
            api_key: API-ключ OpenAI
            base_url: Базовый URL API (для локальных моделей)
            model: Имя модели
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов в ответе
            timeout: Таймаут запроса в секундах
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("LLM_MODEL", self.DEFAULT_MODEL)
        self.temperature = float(os.getenv("LLM_TEMPERATURE", temperature))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", max_tokens))
        self.timeout = int(os.getenv("LLM_TIMEOUT", timeout))

        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY не задан. Укажите ключ в .env "
                "(см. README → Настройка LLM)."
            )

        try:
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError(
                "Пакет openai не установлен. "
                "Выполните: pip install -r requirements.txt"
            ) from e

        self._client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)
        logger.info(
            "OpenAILLMClient инициализирован: model=%s, base_url=%s, timeout=%ds",
            self.model,
            self.base_url,
            self.timeout,
        )

    def generate(self, prompt: str, *, system: Optional[str] = None) -> str:
        """Генерирует ответ с помощью OpenAI-совместимого API.
        
        Args:
            prompt: Пользовательский промпт с контекстом
            system: Системный промпт (опционально)
            
        Returns:
            Сгенерированный текст ответа
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error("Ошибка вызова OpenAI API: %s", e)
            return f"Ошибка при генерации ответа: {str(e)}"


class OllamaLLMClient:
    """Специализированный клиент для Ollama с оптимизированными настройками.

    Требует:
        OLLAMA_BASE_URL — базовый URL Ollama API (по умолчанию http://localhost:11434/v1)
    Опционально:
        OLLAMA_MODEL — имя модели (по умолчанию qwen2.5-coder:32b-instruct)
        LLM_TEMPERATURE
        LLM_MAX_TOKENS
        LLM_TIMEOUT — таймаут в секундах (по умолчанию 120)
    """

    DEFAULT_MODEL = OLLAMA_DEFAULT_MODEL
    DEFAULT_BASE_URL = OLLAMA_BASE_URL

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 800,
        timeout: int = 120,
    ):
        """Инициализация клиента Ollama.
        
        Args:
            base_url: Базовый URL Ollama API
            model: Имя модели Ollama
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов в ответе
            timeout: Таймаут запроса в секундах
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", self.DEFAULT_BASE_URL)
        self.model = model or os.getenv("OLLAMA_MODEL", os.getenv("LLM_MODEL", self.DEFAULT_MODEL))
        self.temperature = float(os.getenv("LLM_TEMPERATURE", temperature))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", max_tokens))
        self.timeout = int(os.getenv("LLM_TIMEOUT", timeout))

        try:
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError(
                "Пакет openai не установлен. "
                "Выполните: pip install -r requirements.txt"
            ) from e

        # Для Ollama можно использовать любой непустой ключ
        self._client = OpenAI(
            base_url=self.base_url,
            api_key="ollama",
            timeout=self.timeout
        )
        
        logger.info(
            "OllamaLLMClient инициализирован: model=%s, base_url=%s, timeout=%ds",
            self.model,
            self.base_url,
            self.timeout,
        )

    def generate(self, prompt: str, *, system: Optional[str] = None) -> str:
        """Генерирует ответ с помощью Ollama.
        
        Args:
            prompt: Пользовательский промпт с контекстом
            system: Системный промпт (опционально)
            
        Returns:
            Сгенерированный текст ответа
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            start_time = time.time()
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            elapsed_time = time.time() - start_time
            logger.debug("Ollama ответил за %.2f секунд", elapsed_time)
            
            if response.choices and response.choices[0].message:
                return response.choices[0].message.content or ""
            else:
                return "Ошибка: пустой ответ от Ollama."
                
        except Exception as e:
            logger.error("Ошибка вызова Ollama API: %s", e)
            return f"Ошибка при генерации ответа Ollama: {str(e)}"


def get_llm_client(provider: Optional[str] = None) -> LLMClient:
    """Фабрика LLM-клиентов.
    
    Определяет провайдера в порядке приоритета:
    1. Явно переданный provider
    2. Переменная окружения LLM_PROVIDER
    3. Конфигурация по умолчанию из config.DEFAULT_LLM_PROVIDER
    4. Автовыбор на основе доступных ключей
    
    Args:
        provider: Имя провайдера (yandex, openai, ollama, stub)
        
    Returns:
        Инициализированный LLM-клиент
    """
    # Определяем провайдера
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", DEFAULT_LLM_PROVIDER)
    
    # Если DEMO_MODE включен, возвращаем демо-режим заглушки
    if DEMO_MODE:
        logger.info("Демо-режим активирован, используется StubLLMClient с демо-ответами")
        return StubLLMClient(demo_mode=True)
    
    # Автовыбор, если provider = "auto" или не указан
    if provider == "auto" or not provider:
        if os.getenv("YANDEX_GPT_API_KEY") and os.getenv("YANDEX_GPT_FOLDER_ID"):
            provider = "yandex"
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        elif os.getenv("OLLAMA_BASE_URL"):
            provider = "ollama"
        else:
            provider = "stub"
    
    # Создаем клиент
    try:
        if provider == "yandex":
            return YandexGPTClient()
        elif provider == "openai":
            return OpenAILLMClient()
        elif provider == "ollama":
            return OllamaLLMClient()
        elif provider == "stub":
            logger.info("Используется StubLLMClient (демо-режим)")
            return StubLLMClient(demo_mode=True)
        else:
            raise ValueError(f"Неизвестный провайдер: {provider}")
    except Exception as e:
        logger.warning("Не удалось инициализировать %s: %s. Используется заглушка.", provider, e)
        return StubLLMClient(demo_mode=True)