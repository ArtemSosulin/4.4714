from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError


class Merchant:
    def __init__(self, merchant_id, name, category, country):
        identifier(merchant_id)
        name = valid_name(name)
        choice(category, ("GROCERY", "RESTAURANT", "FUEL", "TRAVEL", "GAMBLING", "OTHER"), "INVALID_CATEGORY")
        valid_country(country)
        self._merchant_id = merchant_id
        self._name = name
        self._category = category
        self._country = country
        self._status = "ACTIVE"

    @property
    def merchant_id(self):
        return self._merchant_id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def country(self):
        return self._country

    @property
    def status(self):
        return self._status

    def suspend(self):
        if self.status not in ('ACTIVE',):
            raise DomainError("INVALID_STATE")
        self._status = "SUSPENDED"

    def activate(self):
        if self.status not in ('SUSPENDED',):
            raise DomainError("INVALID_STATE")
        self._status = "ACTIVE"

    def close(self):
        if self.status not in ('ACTIVE', 'SUSPENDED'):
            raise DomainError("INVALID_STATE")
        self._status = "CLOSED"

    def availability(self): # Проверяем, находится ли магазин в активном состоянии.# Только ACTIVE означает, что магазин доступен для операций.
        if self.status != "ACTIVE":
            # Если магазин неактивен, возвращаем отказ.
            # Для NEW используем код MERCHANT_NOT_ACTIVE.
            # Для остальных состояний сохраняем соответствующий код.
            return CheckResult(
                False,
                "MERCHANT_" + (
                    "NOT_ACTIVE" if self.status == "NEW"
                    else self.status
                )
            )

        # Если магазин активен, разрешаем операцию.
        return CheckResult(True)

    def describe(self):
        return f"{self.merchant_id}:{self.name}:{self.category}:{self.status}"


