# Merchant: справка для ЛР3

Магазин хранит категорию, страну и статус обслуживания. Сервис проверяет, разрешена ли операция в заданном канале.

Здесь перечислены типы текущей работы. Что требуется реализовать и какие файлы можно менять, указано в [TASK.md](TASK.md).

## Предметные объекты и исполнители

| Тип и конструктор | Публичные действия и свойства | Файл |
|---|---|---|
| `MerchantAcceptanceRule()` | `check(entity, context)` | `app/domain/acceptance.py` |
| `RestrictedCategoryRule(values)` | `check(entity, context)` | `app/domain/acceptance.py` |
| `AcceptedChannelRule(values)` | `check(entity, context)` | `app/domain/acceptance.py` |
| `Merchant(merchant_id, name, category, country)` | `merchant_id`, `name`, `category`, `country`, `status`, `suspend()`, `activate()`, `close()`, `availability()` | `app/domain/merchant.py` |

Свойства читаются без скобок. Поля объекта-значения не меняются присваиванием; результат операции создаётся отдельно. Для наследника без собственного конструктора показаны аргументы конструктора базового класса.

## Вызов сервиса

| Метод | Сигнатура |
|---|---|
| `__init__` | `MerchantService(repository, rules=())` |
| `register` | `register(entity)` |
| `get` | `get(key)` |
| `suspend` | `suspend(key)` |
| `activate` | `activate(key)` |
| `close` | `close(key)` |
| `check` | `check(key, context)` |

`app/api.py` — готовая внешняя граница; не изменяйте её. Вызов попадает в сервис из указанного модуля. Подробные примеры создания входных объектов находятся в открытых тестах текущей папки.

Состав исполнителей в этой заготовке задан. Функция сборки уже готова; `app/services/assembly.py` не меняется. Задача — реализовать общий вызов и распределить поведение между указанными объектами.

## Готовые результаты и ошибки

`DomainError` находится в `app/support/errors.py`; код доступен через `error.code`. В разрешённых методах используйте готовые проверки, а не новую иерархию исключений.

`CheckResult(True)` означает разрешение. `CheckResult(False, code)` означает отказ, а не изменение статуса объекта. Некорректный тип результата правила вызывает `INVALID_RESULT`. При записи или списании сервис преобразует предусмотренный отказ в `DomainError` до изменения данных.

## Проверка поведения

`tests/test_contract.py` и `tests/test_review_contract.py` проверяют предметные правила. `tests/test_progression.py` проверяет последовательности обращений и настройки текущей работы. Ни один результат теста не является командой менять защищённый API или тесты.

Ожидаемый стартовый результат — в [STARTER-STATE.md](STARTER-STATE.md). Проверка из корня проекта: `python check.py lab03`.
