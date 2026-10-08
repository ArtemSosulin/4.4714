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

def make_entity(*args, **kwargs):
    return Merchant(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'merchant_id': entity.merchant_id, 'name': entity.name, 'category': entity.category, 'country': entity.country, 'status': entity.status}


from app.support.types import Repository

def new_service(repository=None):
    return MerchantService(repository if repository is not None else Repository("merchant_id"))
