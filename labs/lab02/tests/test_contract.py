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

from app.support.types import MerchantContext

def context():
    return MerchantContext()

def entity(key='M1'):
    return api.make(key, "Coffee", "RESTAURANT", "NL")

def prepared(key='M1'):
    service = api.create()
    item = entity(key)
    invoke(service, "register", item)
    return service, item

def test_basic_lifecycle_and_isolation():
    service, item = prepared()
    other = entity("OTHER")
    invoke(service, "register", other)
    assert invoke(service, "check", 'M1', context()).allowed
    invoke(service, 'suspend', 'M1')
    assert invoke(service, "check", 'M1', context()).code == 'MERCHANT_SUSPENDED'
    assert api.view(other)["status"] == 'ACTIVE'
    invoke(service, 'activate', 'M1')
    assert invoke(service, "check", 'M1', context()).allowed
    assert invoke(service, "get", 'M1') is item

def test_repositories_are_independent():
    service, item = prepared()
    error("NOT_FOUND", lambda: invoke(api.create(), "get", 'M1'))

def test_checks_do_not_change_entity():
    service, item = prepared()
    before = api.view(item)
    invoke(service, "check", 'M1', context())
    invoke(service, "check", 'M1', context())
    assert api.view(item) == before

def test_closed_is_terminal():
    service, item = prepared()
    item.close()
    error("INVALID_STATE", item.activate)
    assert item.status == "CLOSED"
    assert invoke(service, "check", 'M1', context()).code == 'MERCHANT_CLOSED'

def test_repeat_pause_does_not_change_status():
    service, item = prepared()
    item.suspend()
    error("INVALID_STATE", item.suspend)
    assert item.status == 'SUSPENDED'

def test_status_is_read_only():
    service, item = prepared()
    with pytest.raises(AttributeError):
        item.status = "CLOSED"
def test_name_is_validated():
    error("INVALID_NAME", lambda: api.make("X", "   ", "RESTAURANT", "NL"))
    assert api.make("X", " Alice ", "RESTAURANT", "NL").name == "Alice"
@pytest.mark.parametrize("code", ["nl", "NLD", "1L"])
def test_country_is_validated(code):
    error("INVALID_COUNTRY", lambda: api.make("X", "Cafe", "RESTAURANT", code))
