from abc import ABC, abstractmethod
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError

class MerchantAcceptanceRule(ABC):
    @abstractmethod
    def check(self, entity, context):
        raise NotImplementedError

class RestrictedCategoryRule(MerchantAcceptanceRule):
    def __init__(self, values):
        self._values = frozenset(values)
        for value in self._values:
            choice(value, ('GROCERY', 'RESTAURANT', 'FUEL', 'TRAVEL', 'GAMBLING', 'OTHER'), "INVALID_CONFIG")

    def check(self, entity, context):
        if entity.category in self._values:
            return CheckResult(False, "MERCHANT_CATEGORY_DENIED")
        return CheckResult(True)

class AcceptedChannelRule(MerchantAcceptanceRule):
    def __init__(self, values, code="MERCHANT_CHANNEL_DENIED"):
        self._values = frozenset(values)
        self._code = code

        for value in self._values:
            choice(value, ("POS", "ONLINE"), code="INVALID_CONFIG")

    def check(self, entity, context):
        if context.channel not in self._values:
            return CheckResult(False, self._code)
        return CheckResult(True)
