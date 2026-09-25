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


from app.support.types import Repository


# Ниже — прежний рабочий путь. Перенесите поведение, затем обновите
# make_entity, invoke, view и new_service: сигнатуры должны сохраниться.
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError

def make_entity(merchant_id, name, category, country):
    return {'merchant_id': merchant_id, 'name': name, 'category': category, 'country': country, "status": "ACTIVE"}

def _new_legacy_service(repository):
    return {"repository": repository}

def view(entity):
    return dict(entity)

def invoke(service, method, *args, **kwargs):
    repository = service["repository"]
    if method == "register":
        return repository.add(args[0])
    entity = repository.get(args[0])
    if method == "get":
        return entity
    if method == "suspend":
        entity["status"] = "SUSPENDED"
        return None
    if method == "activate":
        entity["status"] = "ACTIVE"
        return None
    if method == "close":
        entity["status"] = "CLOSED"
        return None
    if method == "check":
        context = args[1]
        if entity["status"] != "ACTIVE":
            return CheckResult(False, "MERCHANT_" + ("NOT_ACTIVE" if entity["status"] == "NEW" else entity["status"]))
        if entity["category"] == "GAMBLING":
            return CheckResult(False, "MERCHANT_CATEGORY_DENIED")
        if context.channel not in {"POS", "ONLINE"}:
            return CheckResult(False, "MERCHANT_CHANNEL_DENIED")
        return CheckResult(True)
    raise ValueError(method)


from app.support.types import Repository

def new_service(repository=None):
    return _new_legacy_service(repository if repository is not None else Repository("merchant_id"))
