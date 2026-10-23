# Исходные проверки ЛР3

Успешных проверок: **16**. Ожидаемых падений: **9**.

Не завершены общий интерфейс, алгоритмы исполнителей и основной метод сервиса. Поэтому один незаполненный метод может вызвать несколько падений — это не несколько независимых задач.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_availability_does_not_cache_state`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_abc_is_abstract`
- `tests.test_contract::test_basic_lifecycle_and_isolation`
- `tests.test_contract::test_checks_do_not_change_entity`
- `tests.test_contract::test_closed_is_terminal`
- `tests.test_contract::test_first_rule_negative_and_immutable_config`
- `tests.test_contract::test_rules_used_by_service`
- `tests.test_contract::test_second_rule_negative`
- `tests.test_review_contract::test_review_empty_deny_set_is_not_empty_allow_set`

## Порядок проверки

Из корня проекта: `python check.py lab03`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
