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

def test_rename_is_atomic():
    item = api.make('M1', "Coffee", "RESTAURANT", "NL")
    previous = item.name
    error("INVALID_NAME", lambda: item.rename(" "))
    assert item.name == previous
    item.rename(" Bob ")
    assert item.name == "Bob"
