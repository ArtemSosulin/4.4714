# ЛР1: заготовленный сервис. Допишите отмеченный метод и подключите объекты.
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository


from app.support.types import name as valid_name, country as valid_country


from app.support.errors import DomainError


from app.domain.merchant import Merchant


class MerchantService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        pass

    def register(self, entity):
        return self._repository.add(entity)

    def get(self, key):
        return self._repository.get(key)

    def suspend(self, key):
        self.get(key).suspend()
    def activate(self, key):
        self.get(key).activate()

    def close(self, key):
        self.get(key).close()

    def check(self, key, context):
        entity = self.get(key)
        result = entity.availability()
        if not result.allowed:
            return result
        if entity.category == "GAMBLING":
            return CheckResult(False, "MERCHANT_CATEGORY_DENIED")
        if context.channel not in {"POS", "ONLINE"}:
            return CheckResult(False, "MERCHANT_CHANNEL_DENIED")
        return CheckResult(True)

from app.domain.merchant import Merchant
from app.support.types import Repository


# Ниже — прежний рабочий путь. Перенесите поведение, затем обновите
# make_entity, invoke, view и new_service: сигнатуры должны сохраниться.
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError

def make_entity(merchant_id, name, category, country):
    return Merchant(merchant_id, name, category, country)

def _new_legacy_service(repository):
    return {"repository": repository}

def view(entity):
    return {
        "merchant_id": entity.merchant_id,
        "name": entity.name,
        "category": entity.category,
        "country": entity.country,
        "status": entity.status,
    }
def invoke(service, method, *args, **kwargs):
    if method == "register":
        return service.register(args[0])

    if method == "get":
        return service.get(args[0])

    if method == "suspend":
        return service.suspend(args[0])

    if method == "activate":
        return service.activate(args[0])

    if method == "close":
        return service.close(args[0])

    if method == "check":
        return service.check(args[0], args[1])

    raise ValueError(method)

from app.support.types import Repository

def new_service(repository=None):
    repository = repository if repository is not None else Repository("merchant_id")
    return MerchantService(repository)