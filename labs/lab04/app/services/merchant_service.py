from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError
from app.domain.merchant import Merchant
from app.domain.acceptance import RestrictedCategoryRule, AcceptedChannelRule

class MerchantService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = [RestrictedCategoryRule({"GAMBLING"}), AcceptedChannelRule({"POS", "ONLINE"})]  # конкретные объекты пока создаются здесь

    def register(self, entity):
        return self._repository.add(entity)

    def get(self, key):
        return self._repository.get(key)


    def suspend(self, key):
        # Получаем магазин из репозитория.
        # Изменение статуса теперь выполняет сам объект Merchant.
        entity = self.get(key)
        entity.suspend()

    def activate(self, key):
        # Активируем магазин через метод объекта,
        # не обращаясь напрямую к приватному атрибуту _status.
        entity = self.get(key)
        entity.activate()

    def close(self, key):
        # Закрываем магазин через метод Merchant.
        # Проверка допустимости перехода выполняется внутри объекта.
        entity = self.get(key)
        entity.close()

    def check(self, key, context):
        entity = self.get(key)

        # Проверяем доступность через availability(),
        # чтобы не дублировать проверку статуса в сервисе.
        availability = entity.availability()
        if not availability.allowed:
            return availability

        # Проверяем правила приема по категории и каналу.
        # При первом нарушении возвращаем соответствующий отказ.
        for rule in self._rules:
            result = checked(rule.check(entity, context))
            if not result.allowed:
                return result

        # Если все проверки пройдены, разрешаем операцию.
        return CheckResult(True)


    def diagnostic(self, key):
        # Получаем магазин из репозитория один раз,
        # чтобы исключить повторный поиск одного объекта.
        entity = self._repository.get(key)
        return entity.name

def make_entity(*args, **kwargs):
    return Merchant(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'merchant_id': entity.merchant_id, 'name': entity.name, 'category': entity.category, 'country': entity.country, 'status': entity.status}


from app.support.types import Repository

def new_service(repository=None):
    return MerchantService(repository if repository is not None else Repository("merchant_id"))
