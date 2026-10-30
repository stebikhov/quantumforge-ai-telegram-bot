import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TERMS_MAP_FILE = str(PROJECT_ROOT / "terms_map.json")
OUTPUT_DIR = str(PROJECT_ROOT / "knowledge_base")

documents = [
    {
        "filename": "01_xarn_velgor.md",
        "title": "# Xarn Velgor — Верховный лорд Void Walkers",
        "content": """
Xarn Velgor — один из самых могущественных лидеров Void Walkers в истории Quantum Realms. Рождённый как Dain Shadowborn на пустынной планете Dustara, он прошёл путь от раба до правителя Central Dominion.

## Биография

Dain Shadowborn родился в 42 году до формирования New Dominion. Его мать, Sera Twilight, умерла при родах. В детстве Dain проявлял необычайные способности к управлению Synth Flux, что привлекло внимание Sentinel Sage Torin Ashenblade.

После обучения в Sentinel Citadel, Dain стал одним из сильнейших Flux Sentinels. Однако страх потери близких и искушение Void Current привели его к падению. Он принял имя Xarn Velgor и стал учеником Supreme Archon Malacor.

## Способности

- Мастерство владения Plasma Edge (красный кристалл)
- Управление Synth Flux на уровне Void Master
- Тактический гений в космических сражениях
- Пилотирование Shadow Interceptor

## Ключевые события

- Участие в Replica Conflicts на стороне Breakaway Systems
- Осада Sentinel Citadel и уничтожение Flux Sentinels
- Строительство Void Core — орбитальной станции с супероружием
- Противостояние с собственным сыном, Kael Stormrunner, над Infernis

## Цитата

> «Ты не понимаешь силы Void Current. Она даёт власть над жизнью и смертью.»
"""
    },
    {
        "filename": "02_kael_stormrunner.md",
        "title": "# Kael Stormrunner — последний Flux Sentinel",
        "content": """
Kael Stormrunner — ключевая фигура в истории Free Systems Coalition. Сын Xarn Velgor (ранее известного как Dain Shadowborn) и неизвестной матери, он был воспитан на Dustara дядей и тётей.

## Ранние годы

Kael вырос на пустынной планете Dustara, мечтая присоединиться к Coalition Forces. Его дядя Owen и тётя Beru держали в секрете его происхождение. Всё изменилось, когда Kael купил двух автоматонов — Beep-7 и Goldstream — у Scrap Scavengers.

## Обучение пути Flux Sentinel

После гибели семьи от рук Dominion Troopers, Kael встретил Torin Ashenblade, который передал ему Plasma Edge его отца и начал обучение. Позже Kael отправился к Elder Mythos на Verdanth, где прошёл углублённое обучение Synth Flux.

## Ключевые достижения

- Уничтожение Void Core во время битвы за Celestara
- Освобождение Rex Voidwalker из Stasis Alloy в Port Shadowsand
- Руководство атакой на Frostveil
- Победа над Xarn Velgor в финальном противостоянии

## Цитата

> «Я Kael Stormrunner, сын Dain Shadowborn. Я — Flux Sentinel Free Systems Coalition.»
"""
    },
    {
        "filename": "03_zara_nightbreeze.md",
        "title": "# Zara Nightbreeze — принцесса Celestara и лидер Coalition",
        "content": """
Zara Nightbreeze — принцесса планеты Celestara, сенатор в United Systems Concord, и одна из ключевых лидеров Free Systems Coalition.

## Происхождение

Дочь королевы Sera Twilight и короля Bail Organa. После уничтожения Celestara имперским супероружием Void Core, Zara посвятила жизнь борьбе против Central Dominion.

## Роль в Coalition

- Координатор операций Underground Network
- Дипломатический представитель Coalition в переговорах с внешними системами
- Пилот и тактик в космических сражениях

## Личная жизнь

Во время событий Replica Conflicts Zara вышла замуж за Rex Voidwalker. У них родились трое детей, один из которых — Kaelen Voidmark — позже пал под влиянием Void Current.

## Цитата

> «Надежда подобна солнцу. Если ты веришь в неё, она всегда найдёт путь к тебе.»
"""
    },
    {
        "filename": "04_rex_voidwalker.md",
        "title": "# Rex Voidwalker — контрабандист и герой Coalition",
        "content": """
Rex Voidwalker — известный Freight Runner, капитан корабля Star Phantom, и один из героев Free Systems Coalition.

## Карьера контрабандиста

До присоединения к Coalition, Rex был известен как один из лучших Freight Runners в Outer Rim. Его корабль Star Phantom — модифицированный YT-1300 — считался одним из самых быстрых судов в галактике.

## Участие в Coalition

- Спасение Zara Nightbreeze из плена Central Dominion
- Участие в атаке на Void Core
- Командование эскадрильей во время битвы за Verdanth
- Освобождение Grrrok из плена Slorg the Bloated

## Характер

Rex известен своим сарказмом, прагматизмом и невероятным везением. Несмотря на первоначальный интерес только к деньгам, он стал преданным членом Coalition.

## Цитата

> «Я не верю в Synth Flux. Я верю в хороший Warp Engine и удачу.»
"""
    },
    {
        "filename": "05_torin_ashenblade.md",
        "title": "# Torin Ashenblade — последний Sentinel Sage",
        "content": """
Torin Ashenblade — один из последних Sentinel Sage эпохи Central Dominion. Наставник Kael Stormrunner и хранитель знаний о Synth Flux.

## Биография

Torin служил в Sentinel Conclave во время Replica Conflicts. После падения United Systems Concord и уничтожения большинства Flux Sentinels, он скрылся на Dustara, чтобы присматривать за сыном Dain Shadowborn.

## Обучение Kael

- Передача Plasma Edge от отца к сыну
- Обучение основам Synth Flux
- Направление Kael к Elder Mythos для завершения обучения

## Философия

Torin придерживался классического учения Flux Sentinels: Synth Flux — это энергия, связывающая все живые существа. Void Current — это тёмная сторона, ведущая к страданиям.

## Цитата

> «Synth Flux окружает нас, проникает в нас, связывает галактику в единое целое.»
"""
    },
    {
        "filename": "06_elder_mythos.md",
        "title": "# Elder Mythos — величайший Sentinel Sage",
        "content": """
Elder Mythos — легендарный Sentinel Sage, обучавший поколения Flux Sentinels на протяжении почти тысячи лет. После падения United Systems Concord он скрылся на болотистой планете Verdanth.

## Мудрость

Elder Mythos известен своими загадочными изречениями и глубоким пониманием Synth Flux. Его обучение включало не только технику владения Plasma Edge, но и философское понимание баланса между Flux Harmony и Void Current.

## Ключевые ученики

- Torin Ashenblade
- Dain Shadowborn (до падения)
- Kael Stormrunner

## Смерть

Elder Mythos умер на Verdanth, передав последние знания Kael Stormrunner перед битвой за Celestara.

## Цитаты

> «Делай или не делай. Не надо пытаться.»

> «Страх — путь к Void Current. Страх ведёт к гневу, гнев ведёт к ненависти, ненависть ведёт к страданиям.»
"""
    },
    {
        "filename": "07_supreme_archon_malacor.md",
        "title": "# Supreme Archon Malacor — император Central Dominion",
        "content": """
Supreme Archon Malacor — последний император Central Dominion, создатель Void Core и тайный Void Master.

## Восхождение к власти

Malacor начинал как сенатор в United Systems Concord. Используя кризис Replica Conflicts, он постепенно сосредоточил в своих руках всю полноту власти, объявив себя Supreme Archon.

## Планеты и проекты

- Строительство Void Core — орбитальной станции с супероружием, способным уничтожать целые планеты
- Создание Dreadnought Cruiser класса Sovereign
- Организация охоты на последних Flux Sentinels

## Обучение Xarn Velgor

Malacor взял Dain Shadowborn в ученики после того, как тот пал под влиянием Void Current. Вместе они планировали уничтожить Underground Network и установить вечный порядок Central Dominion.

## Цитата

> «Synth Flux — это путь к силе, недоступной большинству. Void Current даёт возможности, о которых Flux Sentinels не смеют мечтать.»
"""
    },
    {
        "filename": "08_void_core.md",
        "title": "# Void Core — орбитальное супероружие Central Dominion",
        "content": """
Void Core — гигантская орбитальная боевая станция Central Dominion, оснащённая супероружием, способным уничтожать целые планеты.

## Технические характеристики

- Диаметр: 160 км
- Экипаж: 265,000 Dominion Troopers, офицеров и техников
- Вооружение: сверхмощный лазер на основе Flux Crystal
- Двигатели: 124 гипердвигателя класса 4

## История создания

Проект Void Core был запущен Supreme Archon Malacor сразу после установления Central Dominion. Строительство велось в секрете в течение 15 лет.

## Уничтожение Celestara

Первое боевое применение Void Core — уничтожение планеты Celestara, родины Zara Nightbreeze. Это событие продемонстрировало мощь станции и укрепило страх перед Central Dominion.

## Уничтожение

Void Core была уничтожена Kael Stormrunner во время битвы за Celestara. Kael, используя Synth Flux, направил Photon Striker в уязвимое место станции — вентиляционную шахту, ведущую к основному реактору.

## Void Core Prime

После уничтожения первой станции, Central Dominion начала строительство Void Core Prime над Verdanth. Вторая станция также была уничтожена Coalition Forces.
"""
    },
    {
        "filename": "09_plasma_edge.md",
        "title": "# Plasma Edge — оружие Flux Sentinels и Void Walkers",
        "content": """
Plasma Edge — энергетическое оружие, используемое Flux Sentinels и Void Walkers. Состоит из рукояти и клинка из чистой плазмы, удерживаемой Synth Flux.

## Конструкция

- Рукоять: металлический цилиндр с кнопкой активации
- Источник энергии: Flux Crystal (Kyber Crystal)
- Клинок: плазменный луч длиной 1-1.3 метра

## Цвета кристаллов

- Синий/зелёный — Flux Sentinels
- Красный — Void Walkers (кристалл «искусственно» окрашен Void Current)
- Фиолетовый — редкие Sentinel Sage (например, Kor Thunderfist)
- Жёлтый — некоторые специализированные Flux Sentinels

## Формы боя

Существует семь классических форм боя на Plasma Edge:
1. Form I — Shii-Cho (базовая)
2. Form II — Makashi (дуэль)
3. Form III — Soresu (защита)
4. Form IV — Ataru (агрессивная)
5. Form V — Shien/Djem So (контратака)
6. Form VI — Niman (баланс)
7. Form VII — Juyo/Vaapad (агрессивная, близкая к Void Current)

## Известные владельцы

- Kael Stormrunner — синий, затем зелёный
- Xarn Velgor — красный
- Torin Ashenblade — синий
- Elder Mythos — зелёный
"""
    },
    {
        "filename": "10_synth_flux.md",
        "title": "# Synth Flux — энергетическая сила Quantum Realms",
        "content": """
Synth Flux — мистическая энергетическая сила, пронизывающая всю галактику Quantum Realms. Она связывает все живые существа и может быть использована теми, кто обладает чувствительностью к ней.

## Две стороны Synth Flux

### Flux Harmony (Светлая сторона)
- Используется Flux Sentinels
- Основана на знаниях, защите и исцелении
- Требует дисциплины и медитации
- Даёт способности: телекинез, предвидение, исцеление, убеждение

### Void Current (Тёмная сторона)
- Используется Void Walkers
- Основана на эмоциях: страхе, гневе, ненависти
- Даёт быструю, но разрушительную силу
- Способности: удушение, молнии Void Current, доминирование

## Обучение

Чувствительные к Synth Flux начинают обучение в детстве. Flux Acolyte (ученик) обучается под руководством Sentinel Sage в течение многих лет.

## Баланс

Пророчество о «Избранном» гласило, что кто-то восстановит баланс Synth Flux, уничтожив Void Walkers. Kael Stormrunner считается тем, кто исполнил это пророчество, бросив Xarn Velgor в лаву на Infernis.

## Цитата Elder Mythos

> «Инструменты войны не важны. Важен тот, кто держит оружие. Synth Flux — это не сила, которую можно контролировать. Это учитель, который показывает путь.»
"""
    },
    {
        "filename": "11_flux_sentinels.md",
        "title": "# Flux Sentinels — хранители мира United Systems Concord",
        "content": """
Flux Sentinels — древний орден воинов-монахов, служивших United Systems Concord в течение тысячи поколений. Они использовали Synth Flux для поддержания мира и справедливости.

## Организация

- **Sentinel Citadel** — штаб-квартира на Nexus Prime
- **Sentinel Conclave** — совет из 12 Sentinel Sage, управляющий орденом
- **Sentinel Sage** — полные члены ордена
- **Flux Acolyte** — ученики

## Обучение

Дети, чувствительные к Synth Flux, забираются в Sentinel Citadel в раннем возрасте. Обучение включает:
- Владение Plasma Edge (7 форм боя)
- Использование Synth Flux (телекинез, предвидение, исцеление)
- Философия Flux Harmony
- Дипломатия и переговоры

## Падение

Во время Replica Conflicts, Supreme Archon Malacor отдал Приказ 66 — секретную команду, заставляющую Replica Soldiers атаковать своих генералов-Flux Sentinels. Большинство членов ордена было уничтожено.

## Наследие

После падения United Systems Concord, лишь несколько Flux Sentinels выжило. Torin Ashenblade и Elder Mythos скрывались, готовя новое поколение для борьбы с Central Dominion.

## Кодекс Flux Sentinels

> «Эмоций нет, есть покой.
> Невежества нет, есть знание.
> Страсти нет, есть безмятежность.
> Смерти нет, есть Synth Flux.»
"""
    },
    {
        "filename": "12_void_walkers.md",
        "title": "# Void Walkers — тёмные пользователи Synth Flux",
        "content": """
Void Walkers — орден пользователей Void Current, служивших Central Dominion. Они противопоставляли себя Flux Sentinels, используя тёмную сторону Synth Flux.

## Организация

- **Supreme Archon** — лидер (Supreme Archon Malacor)
- **Void Master** — полные члены ордена (например, Xarn Velgor)
- **Ученики** — те, кто находится на пути к Void Mastery

## Философия

Void Walkers верят, что Void Current даёт истинную силу. Они используют эмоции — страх, гнев, ненависть — как источник мощности. В отличие от Flux Sentinels, которые стремятся к покою, Void Walkers принимают страсти.

## Обучение

- Владение Plasma Edge (красный кристалл)
- Техники Void Current: удушение, молнии, доминирование разума
- Тактика ведения боя и управления страхом

## База операций

Void Walkers имели цитадель на Infernis, вулканической планете, где Dain Shadowborn был побеждён Torin Ashenblade.

## Конец ордена

После уничтожения Void Core Prime и смерти Supreme Archon Malacor, орден Void Walkers практически прекратил существование. Лишь отдельные выжившие продолжали действовать в тени.
"""
    },
    {
        "filename": "13_star_phantom.md",
        "title": "# Star Phantom — самый быстрый корабль в галактике",
        "content": """
Star Phantom — лёгкий грузовой корабль класса YT-1300, принадлежащий Rex Voidwalker. Считается одним из самых быстрых судов в Quantum Realms.

## Модификации

Rex Voidwalker внес множество нелегальных модификаций:
- Ускоренные Warp Engines (класс 0.5)
- Усиленные щиты
- Скрытые отсеки для контрабанды
- Модифицированные Pulse Guns

## Экипаж

- Rex Voidwalker — капитан
- Grrrok — второй пилот и штурман
- Зара Nightbreeze — временный член экипажа
- Kael Stormrunner — временный пассажир

## Ключевые миссии

- Побег с Dustara от Dominion Troopers
- Доставка Flux Acolyte Kael Stormrunner к Elder Mythos
- Проникновение на Void Core для спасения Zara Nightbreeze
- Участие в битве за Celestara

## Легенда

Star Phantom известен тем, что прошёл через астероидное поле, уклонился от множества Shadow Interceptors и даже пережил прямое попадание Pulse Gun. Корабль стал символом надежды для Free Systems Coalition.

## Цитата Rex Voidwalker

> «Она может показаться старой развалиной, но Star Phantom никогда меня не подводил.»
"""
    },
    {
        "filename": "14_photon_striker.md",
        "title": "# Photon Striker — истребитель Free Systems Coalition",
        "content": """
Photon Striker — основной истребитель Free Systems Coalition, разработанный для борьбы с Shadow Interceptors Central Dominion.

## Технические характеристики

- Экипаж: 1 пилот + 1 астромеханик-автоматон (Beep-7 тип)
- Вооружение: 4 лазерные пушки, 2 протонные торпеды
- Двигатели: 2 субсветовых двигателя + гипердвигатель
- Щиты: дефлекторные

## Тактика

Photon Strikers используют формацию «X» при атаке, что даёт им превосходство в манёвренности. Их основная тактика — быстрые удары и отход.

## Известные пилоты

- Kael Stormrunner — уничтожил Void Core
- Ace Voidhawk — лидер эскадрильи Rogue Squadron
- Zara Nightbreeze — участвовала в битве за Verdanth

## Битва за Celestara

Во время атаки на Void Core, Photon Strikers провели серию атак на вентиляционные шахты станции. Kael Stormrunner, используя Synth Flux, направил свои торпеды в главный реактор, уничтожив станцию.

## Модификации

Каждый пилот настраивает свой Photon Striker индивидуально. Kael добавил усиленные щиты и улучшенные сенсоры. Ace Voidhawk модифицировал двигатели для ещё большей манёвренности.
"""
    },
    {
        "filename": "15_free_systems_coalition.md",
        "title": "# Free Systems Coalition — сопротивление Central Dominion",
        "content": """
Free Systems Coalition — военный альянс планет и организаций, противостоящих Central Dominion.

## Основание

Coalition была основана Zara Nightbreeze и Bail Organa после уничтожения Celestara. Первоначально это была небольшая сеть Underground Network, которая со временем превратилась в полноценную военную силу.

## Структура

- **Командование** — Zara Nightbreeze, генералы Coalition Forces
- **Flux Sentinels** — Torin Ashenblade, Kael Stormrunner, Elder Mythos
- **Эскадрильи** — Photon Strikers под командованием Ace Voidhawk
- **Наземные силы** — пехота Coalition

## База

Основная база Coalition располагалась на Frostveil — ледяной планете в Outer Rim. После эвакуации с Frostveil, база была перенесена на Verdanth.

## Ключевые победы

- Уничтожение Void Core (битва за Celestara)
- Уничтожение Void Core Prime (битва за Verdanth)
- Смерть Supreme Archon Malacor
- Падение Central Dominion

## Поддержка

Coalition получала поддержку от Commerce Guild, некоторых нейтральных систем и контрабандистов вроде Rex Voidwalker.

## Флаг

Флаг Coalition — белая звезда на синем фоне, символизирующая надежду среди тьмы Central Dominion.
"""
    },
    {
        "filename": "16_central_dominion.md",
        "title": "# Central Dominion — галактическая империя",
        "content": """
Central Dominion — авторитарное государство, пришедшее на смену United Systems Concord после Replica Conflicts.

## История создания

Supreme Archon Malacor использовал кризис Replica Conflicts для концентрации власти. Объявив United Systems Concord неспособным защитить граждан, он распустил сенат и провозгласил Central Dominion.

## Структура власти

- **Supreme Archon** — абсолютный правитель
- **Imperial Senate** — формальный орган (распущен после строительства Void Core)
- **Regional Governors** — управляют системами
- **Military Command** — армия и флот

## Вооружённые силы

- **Dominion Troopers** — пехота в белой броне
- **Shadow Interceptors** — космические истребители
- **Dreadnought Cruisers** — крупные боевые корабли
- **Quad Walkers** — шагающие танки

## Проекты

- Void Core — орбитальное супероружие
- Void Core Prime — вторая, более мощная станция
- Охота на Flux Sentinels (Приказ 66)

## Падение

После уничтожения Void Core Prime и смерти Supreme Archon Malacor, Central Dominion начал распадаться. Underground Network превратилась в New Republic.
"""
    },
    {
        "filename": "17_dustara.md",
        "title": "# Dustara — пустынная планета, родина Xarn Velgor и Kael Stormrunner",
        "content": """
Dustara — пустынная планета в Outer Rim, известная своими двумя солнцами и экстремальными условиями.

## География

- Пустыни: Великое Море Песков, Западные Дюны
- Города: Port Shadowsand (главный космопорт)
- Население: люди, Scrap Scavengers, Sand Stalkers

## Экономика

Dustara — центр контрабанды и нелегальной торговли. Freight Runners вроде Rex Voidwalker часто заходят в Port Shadowsand для сделок со Slorg the Bloated.

## Обитатели

- **Sand Stalkers** — кочевые воины пустыни
- **Scrap Scavengers** — мелкие торговцы запчастями
- **Thunderbeast** — крупные травоядные, используемые Sand Stalkers как транспорт

## Известные уроженцы

- Dain Shadowborn (Xarn Velgor) — родился в рабстве
- Kael Stormrunner — вырос на ферме влаги дяди Owen

## Климат

Два солнца создают экстремальные температуры: днём до +50°C, ночью до -20°C. Вода — самый ценный ресурс.

## Cantina

Nebula Lounge в Port Shadowsand — место встреч контрабандистов, Track Hunters и искателей приключений. Именно здесь Torin Ashenblade встретил Kael Stormrunner.
"""
    },
    {
        "filename": "18_nexus_prime.md",
        "title": "# Nexus Prime — столица Central Dominion и United Systems Concord",
        "content": """
Nexus Prime — столица Central Dominion, город-планета, бывший политический центр United Systems Concord.

## Определение

Nexus Prime — столица Central Dominion после переворота Supreme Archon Malacor. До этого Nexus Prime была столицей United Systems Concord. После падения Central Dominion Nexus Prime стала столицей New Concord.

## География

Вся поверхность планеты покрыта мегаполисом с населением в триллионы. Уровни города уходят на километры вглубь.

## Политическая роль

- Штаб United Systems Concord (сенат, правительство)
- Sentinel Citadel — резиденция Flux Sentinels
- Столица Central Dominion (после переворота Malacor)

## Ключевые локации

- **Сенат** — здание, где Supreme Archon Malacor объявил о создании Central Dominion
- **Sentinel Citadel** — разрушена во время Приказа 66
- **Уровни подполья** — место обитания преступников и Automaton-рабочих

## Население

- Люди различных рас
- Automaton (дроны) — рабочая сила
- Различные инопланетные виды

## После падения Central Dominion

Nexus Prime — столица Central Dominion, а после её падения — столица New Concord, восстановив демократическое правление.
"""
    },
    {
        "filename": "19_frostveil.md",
        "title": "# Frostveil — ледяная планета, база Free Systems Coalition",
        "content": """
Frostveil — ледяная планета в Outer Rim, служившая главной базой Free Systems Coalition.

## Климат

- Температура: от -40°C до -80°C
- Ледяные равнины, горные хребты
- Частые ледяные штормы

## Фауна

- **Frost Strider** — травоядные, используемые Coalition как транспорт
- **Ice Predator** — хищники, опасные для одиночных патрулей

## База Coalition

Coalition построила подземную базу в ледяных пещерах. База включала:
- Ангары для Photon Strikers
- Жилые помещения
- Командный центр
- Медицинский отсек с Regen Pods

## Битва за Frostveil

Central Dominion обнаружил базу Coalition и отправил атаку с Quad Walkers и Dominion Troopers. Coalition понесла потери, но основные силы успели эвакуироваться на Verdanth.

## Эвакуация

Kael Stormrunner, используя Synth Flux, удерживал дверь базы, пока остальные эвакуировались. Его подобрали на Star Phantom.
"""
    },
    {
        "filename": "20_verdanth.md",
        "title": "# Verdanth — лесная планета, дом Elder Mythos",
        "content": """
Verdanth — лесная планета в Mid Rim, известная своей густой растительностью и разнообразной фауной.

## География

- Густые леса с деревьями высотой до 100 метров
- Реки и озёра
- Пещеры и подземные системы

## Население

- **Twiggles** — маленькие меховые существа, живущие в деревьях
- Несколько человеческих колоний

## Роль в истории

Elder Mythos скрывался на Verdanth после падения United Systems Concord. Именно здесь Kael Stormrunner прошёл завершающую стадию обучения Synth Flux.

## Битва за Verdanth

Central Dominion начал строительство Void Core Prime над Verdanth. Coalition Forces атаковали станцию, используя данные от разведчиков Underground Network.

- Photon Strikers атаковали защитные сооружения
- Наземные силы Coalition сражались с Dominion Troopers
- Twiggles помогли, используя примитивное оружие против захватчиков

## Исход

Void Core Prime была уничтожена. Supreme Archon Malacor погиб от рук Kael Stormrunner. Central Dominion начал распадаться.
"""
    },
    {
        "filename": "21_infernis.md",
        "title": "# Infernis — вулканическая планета, место падения Dain Shadowborn",
        "content": """
Infernis — вулканическая планета в Outer Rim, известная своими реками лавы и экстремальными условиями.

## География

- Активные вулканы
- Реки и озёра лавы
- Чёрные скалистые равнины
- Температура поверхности: 200-500°C

## Ключевые события

### Дуэль Dain Shadowborn и Torin Ashenblade

Во время Replica Conflicts, Dain Shadowborn (ещё не ставший Xarn Velgor) сразился со своим бывшим наставником Torin Ashenblade на склонах вулкана. Torin победил, отрубив Dain конечности. Dain упал в лаву, но был спасён Supreme Archon Malacor.

### Финальное противостояние

Годы спустя, Kael Stormrunner сразился с Xarn Velgor на Infernis. Kael победил, но отказался убить своего отца. Xarn Velgor, увидев страдания сына, повернулся против Supreme Archon Malacor, спасая Kael. Это исполнило пророчество о восстановлении баланса Synth Flux.

## Цитата Kael Stormrunner

> «Я — Flux Sentinel, как и мой отец до меня. Я не буду убивать тебя, Xarn Velgor. Ты уже мёртв.»
"""
    },
    {
        "filename": "22_celestara.md",
        "title": "# Celestara — планета-рай, уничтоженная Void Core",
        "content": """
Celestara — красивая планета в Core Worlds, родина Zara Nightbreeze и столица United Systems Concord.

## География

- Озёра и реки
- Зелёные равнины
- Города с элегантной архитектурой
- Подводные города Gungan-подобной расы Aquarians

## Политика

Celestara была представлена в сенате United Systems Concord королевой Sera Twilight, а затем её дочерью Zara Nightbreeze.

## Уничтожение

Central Dominion использовал Void Core для первого демонстрационного выстрела. Целем стала Celestara — символ сопротивления Central Dominion. Планета была полностью уничтожена, погибли миллиарды.

## Последствия

Уничтожение Celestara укрепило решимость Free Systems Coalition бороться против Central Dominion. Zara Nightbreeze посвятила жизнь уничтожению Void Core.

## Цитата Zara Nightbreeze

> «Celestara была моим домом. Её больше нет. Но пока есть те, кто борется за свободу, надежда жива.»
"""
    },
    {
        "filename": "23_replica_conflicts.md",
        "title": "# Replica Conflicts — галактическая война",
        "content": """
Replica Conflicts — трёхлетняя галактическая война между United Systems Concord и Breakaway Systems.

## Причины

Commerce Guild и другие корпорации недовольные налогами и регулированием United Systems Concord, создали Breakaway Systems. Они построили армию Combat Automatons под руководством Warlord Kryx.

## Ход войны

- Битва на Crystalline Depths — начало конфликтов
- Сражения на множестве планет
- Dain Shadowborn перешёл на сторону Breakaway Systems
- Flux Sentinels вели армию Concord Forces

## Приказ 66

В финале войны, Supreme Archon Malacor отдал Приказ 66 — секретную команду Replica Soldiers атаковать своих генералов-Flux Sentinels. Большинство Flux Sentinels погибло.

## Исход

Breakaway Systems были побеждены. United Systems Concord трансформировалась в Central Dominion. Supreme Archon Malacor стал абсолютным правителем.

## Потери

- Миллиарды погибших
- Уничтожение ордена Flux Sentinels
- Конец демократии в галактике
"""
    },
    {
        "filename": "24_grrrok.md",
        "title": "# Grrrok — верный компаньон Rex Voidwalker",
        "content": """
Grrrok — Furrian, второй пилот Star Phantom и ближайший друг Rex Voidwalker.

## Происхождение

Grrrok родился на лесной планете Grovetree. Во время Clone Wars, его народ был порабощён Commerce Guild. Rex Voidwalker освободил Grrrok, и с тех пор они стали неразлучны.

## Роль

- Второй пилот Star Phantom
- Механик (несмотря на репутацию Furrians как «непонимающих в технике»)
- Ближний бой (использует лук и арбалет)

## Характер

Grrrok известен своей преданностью, силой и умением выражать эмоции через рычание. Rex Voidwalker понимает его без перевода.

## Ключевые моменты

- Освобождение из плена Slorg the Bloated
- Участие в битве за Verdanth
- Помощь Kael Stormrunner в обучении управлению Synth Flux

## Цитата

(Рычание, переведённое Rex Voidwalker)
> «Мы в этой заднице по уши, и это мне нравится.»
"""
    },
    {
        "filename": "25_battle_droids.md",
        "title": "# Combat Automatons — армия Breakaway Systems",
        "content": """
Combat Automatons — массово производимые боевые дроиды, служившие армией Breakaway Systems во время Replica Conflicts.

## Типы

### Standard Combat Automaton
- Рост: 1.9 метра
- Вооружение: Pulse Gun
- Броня: лёгкая белая
- Интеллект: базовый ИИ

### Heavy Combat Automaton
- Рост: 2.1 метра
- Вооружение: двойные Pulse Guns, встроенные в руки
- Броня: усиленная серая
- Интеллект: продвинутый ИИ

### Destroyer Droid
- Форма: трёхколёсная платформа
- Вооружение: скорострельные бластеры, щиты
- Тактика: окружение и подавление

## Производство

Combat Automatons производились на фабриках Commerce Guild на Crystalline Depths. Их создавали миллионами для войны против United Systems Concord.

## Слабости

- Низкая точность стрельбы
- Предсказуемая тактика
- Уязвимость к EMP
- Отсутствие инициативы

## Наследие

После Replica Conflicts, большинство Combat Automatons было выведено из строя. Некоторые были перепрограммированы для мирных целей.
"""
    },
    {
        "filename": "26_slorg_the_bloated.md",
        "title": "# Slorg the Bloated — криминальный босс Port Shadowsand",
        "content": """
Slorg the Bloated — могущественный криминальный босс, контролирующий Port Shadowsand на Dustara.

## Внешность

Slorg — представитель расы Hutt, гигантский слизнеподобный гуманоид длиной около 10 метров. Его тело покрыто слизью, а глаза выдают хитрый ум.

## Империя

- Контрабанда оружия и запрещённых технологий
- Нелегальные гонки на Turbo Sleds
- Торговля информацией
- Работорговля (включая заморозку в Stasis Alloy)

## Резиденция

Slorg живёт в огромном дворце за пределами Port Shadowsand. В его тронном зале постоянно присутствуют охранники, танцовщицы и просители.

## Отношения с Rex Voidwalker

Rex Voidwalker задолжал Slorg крупную сумму после того, как выбросил груз при встрече с Dominion Troopers. Slorg нанял Track Hunter Karr Vex, чтобы вернуть долг.

## Падение

Zara Nightbreeze, притворившись охотницей за головами, освободила Rex Voidwalker из Stasis Alloy. Grrrok убил Slorg в последовавшей схватке.

## Цитата

> «Rex Voidwalker, ты мне должен. И я всегда получаю своё.»
"""
    },
    {
        "filename": "27_karr_vex.md",
        "title": "# Karr Vex — легендарный Track Hunter",
        "content": """
Karr Vex — самый известный Track Hunter в Quantum Realms, известный своей бронёй из сплава Mandalorian и невероятной эффективностью.

## Броня

Броня Karr Vex изготовлена из сплава Iron Clan Warriors — материала, способного выдержать прямое попадание Plasma Edge. Шлем оснащён продвинутыми сенсорами и системой прицеливания.

## Вооружение

- Pulse Gun с различными типами боеприпасов
- Огнемёт
- Ракетница на плече
- Скрытые лезвия на запястьях
- Тросомёт

## Известные контракты

- Охота на Flux Sentinels (во время Приказа 66)
- Поимка Rex Voidwalker для Slorg the Bloated
- Охота на Kael Stormrunner по приказу Xarn Velgor

## Философия

Karr Vex следует кодексу Iron Clan Warriors: честь, верность слову, защита клана. Он не присоединился ни к Central Dominion, ни к Free Systems Coalition, оставаясь нейтральным.

## Исчезновение

После встречи с Kael Stormrunner на Verdanth, Karr Vex исчез. Ходят слухи, что он видел истинное лицо Central Dominion и пересмотрел свои приоритеты.

## Цитата

> «Я Track Hunter. Я всегда нахожу свою цель.»
"""
    },
    {
        "filename": "28_sentinel_citadel.md",
        "title": "# Sentinel Citadel — штаб ордена Flux Sentinels",
        "content": """
Sentinel Citadel — древняя крепость Flux Sentinels, расположенная на Nexus Prime.

## Архитектура

- Башни из белого камня
- Сады для медитации
- Библиотека с древними Memory Crystals
- Тренировочные залы
- Зал Conclave для заседаний совета

## Функции

- Обучение Flux Acolytes
- Хранение Memory Crystals с записями тысячелетий
- Совет Sentinel Conclave принимает решения
- Архивы с информацией о Synth Flux

## Падение

Во время Приказа 66, Replica Soldiers штурмовали Sentinel Citadel. Большинство Flux Sentinels, включая детей, было убито. Лишь немногие выжили, включая Torin Ashenblade.

## После падения Central Dominion

Руины Sentinel Citadel стали мемориалом павшим Flux Sentinels. New Republic планирует восстановить цитадель как символ возрождения демократии.

## Цитата Torin Ashenblade

> «Sentinel Citadel был не просто зданием. Это был символ надежды для всей галактики. Мы вернём её.»
"""
    },
    {
        "filename": "29_memory_crystal.md",
        "title": "# Memory Crystal — хранилище знаний Flux Sentinels",
        "content": """
Memory Crystal — устройство хранения данных, используемое Flux Sentinels для записи и передачи знаний.

## Конструкция

- Кристаллическая структура, содержащая голографические данные
- Активируется Synth Flux
- Может хранить терабайты информации

## Использование

- Запись исторических событий
- Хранение техник боя на Plasma Edge
- Сохранение философских учений о Synth Flux
- Передача знаний между поколениями Flux Sentinels

## Доступ

Только Flux Sentinels и Flux Acolytes могут активировать Memory Crystals с помощью Synth Flux. Для других это просто красивые кристаллы.

## Известные Memory Crystals

- **Кристалл Elder Mythos** — содержит его личные записи и учения
- **Кристалл Sentinel Conclave** — протоколы заседаний совета
- **Кристалл форм боя** — все семь классических форм

## После падения

Многие Memory Crystals были уничтожены или украдены во время Приказа 66. Torin Ashenblade сохранил несколько кристаллов, которые передал Kael Stormrunner.
"""
    },
    {
        "filename": "30_warp_engine.md",
        "title": "# Warp Engine — технология гиперпространственных прыжков",
        "content": """
Warp Engine — устройство, позволяющее космическим кораблям путешествовать быстрее скорости света через Warp Void.

## Принцип работы

Warp Engine создаёт поле, которое смещает корабль в Warp Void — параллельное измерение, где расстояние между точками значительно короче. После выхода из Warp Void, корабль возвращается в нормальное пространство.

## Классы

- Класс 1 — базовый (медленный, используется грузовыми судами)
- Класс 0.5 — средний (торговые суда, корветы)
- Класс 0.3 — быстрый (истребители, курьерские суда)
- Класс 0.1 — экспериментальный (Star Phantom Rex Voidwalker)

## Риски

- Столкновение с гравитационными аномалиями
- Потеря навигационных данных
- Повреждение двигателя при неправильном выходе

## История

Warp Engine были изобретены тысячи лет назад и стали основой для исследования Quantum Realms. Без них галактическая цивилизация была бы невозможна.

## Будущее

Учёные United Systems Concord исследовали возможность создания «коридоров» в Warp Void для мгновенных путешествий между системами. Эти исследования были засекречены Central Dominion.
"""
    },
    {
        "filename": "31_pulse_gun.md",
        "title": "# Pulse Gun — стандартное оружие галактики",
        "content": """
Pulse Gun — энергетическое оружие, используемое во всей галактике Quantum Realms.

## Типы

### Military Pulse Gun
- Используется Dominion Troopers и Coalition Forces
- Режимы: одиночный, автоматический
- Эффективная дальность: 300 метров

### Heavy Pulse Gun
- Используется Heavy Combat Automatons
- Увеличенная мощность и скорострельность
- Требует установки на штатив или бронированную платформу

### Sport Pulse Gun
- Гражданская версия с ограниченной мощностью
- Используется для охоты и самообороны

## Боеприпасы

Pulse Gun использует энергетические ячейки, которые перезаряжаются или заменяются. Одна ячейка содержит достаточно энергии для 500 выстрелов.

## Модификации

- Прицелы (оптические, тепловизоры)
- Глушители
- Увеличенные магазины
- Подствольные гранатомёты

## Известные пользователи

- Rex Voidwalker — модифицированный DL-44
- Dominion Troopers — стандартный E-11
- Kael Stormrunner — захваченный у Dominion Troopers
"""
    },
    {
        "filename": "32_stormtrooper.md",
        "title": "# Dominion Troopers — армия Central Dominion",
        "content": """
Dominion Troopers — элитные солдаты Central Dominion, известные своей белой бронёй и безоговорочной преданностью.

## Обучение

Dominion Troopers проходят жёсткую подготовку с детства. Их учат сражаться, подчиняться приказам и не задавать вопросов. Индивидуальность подавляется ради единства.

## Броня

- Белая пластинчатая броня
- Шлем с системой жизнеобеспечения
- Защита от Pulse Gun попаданий
- Встроенный комлинк

## Вооружение

- Стандартный E-11 Pulse Gun
- Термальные детонаторы
- Штурмовые щиты (для спецподразделений)

## Подразделения

- **Пехота** — стандартные Dominion Troopers
- **Штурмовики** — элитные войска с чёрной маркировкой
- **Снежные штурмовики** — специализированы для Frostveil
- **Огненные штурмовики** — с огнемётами
- **Разведчики** — на Hover Glides

## Репутация

Несмотря на численность, Dominion Troopers известны своей низкой точностью стрельбы против главных героев. Это объясняется «сюжетной бронёй» и неумением стрелять в критические моменты.

## После падения Central Dominion

Многие Dominion Troopers были интегрированы в New Republic Defense Force после прохождения переподготовки.
"""
    }
]

def load_terms_map():
    with open(TERMS_MAP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def replace_terms(text, terms):
    for original, replacement in terms.items():
        text = text.replace(original, replacement)
        text = text.replace(original.lower(), replacement.lower())
    return text

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = load_terms_map()
    terms = data["terms"]

    for doc in documents:
        content = doc["content"]
        replaced = replace_terms(content, terms)

        filepath = os.path.join(OUTPUT_DIR, doc["filename"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(doc["title"] + "\n\n")
            f.write(replaced)

    print(f"Создано {len(documents)} документов в папке {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
