import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.merchant import Merchant
from app.support.types import MerchantContext

def test_progression_availability_does_not_cache_state():
    service = api.create()
    item = Merchant("C", "Cafe", "RESTAURANT", "NL")

    service.register(item)
    first = service.check("C", MerchantContext())
    assert first.allowed
    item.suspend()
    assert service.check("C", MerchantContext()).code == "MERCHANT_SUSPENDED"
    item.activate()
    assert service.check("C", MerchantContext()).allowed
    assert first.allowed and item.status == "ACTIVE"
