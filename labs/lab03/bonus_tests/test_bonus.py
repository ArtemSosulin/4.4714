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

from app.domain.acceptance import AcceptedChannelRule
from app.support.types import MerchantContext

def test_configured_code():
    item = api.make('M1', "Coffee", "RESTAURANT", "NL")
    assert AcceptedChannelRule(set(), code="CUSTOM").check(item, MerchantContext()).code == "CUSTOM"
