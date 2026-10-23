from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError
from app.domain.merchant import Merchant
from app.domain.acceptance import RestrictedCategoryRule, AcceptedChannelRule

class MerchantService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = list(rules) if rules else [
            RestrictedCategoryRule({"GAMBLING"}),
            AcceptedChannelRule({"POS", "ONLINE"})
        ] # конкретные объекты пока создаются здесь

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
        merchant = self.get(key)

        result = merchant.availability()
        if not result.allowed:
            return result

        for rule in self._rules:
            result = checked(rule.check(merchant, context))
            if not result.allowed:
                return result

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
