import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError
from app.support.types import Repository, CheckResult, Money, money


def error(code, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == code


def invoke(service, method, *args, **kwargs):
    return api.call(service, method, *args, **kwargs)

from app.domain.merchant import Merchant

def test_description():
    item = Merchant("M1", "Coffee", "RESTAURANT", "NL")
    assert item.describe() == 'M1:Coffee:RESTAURANT:ACTIVE'
