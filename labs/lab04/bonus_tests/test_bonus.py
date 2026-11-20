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

def test_single_lookup(monkeypatch):
    item = api.make('M1', "Coffee", "RESTAURANT", "NL")
    repository = Repository('merchant_id')
    repository.add(item)
    service = api.create(repository=repository)
    calls=[]
    original=repository.get
    def get(key):
        calls.append(key)
        return original(key)
    monkeypatch.setattr(repository,"get",get)
    service.diagnostic('M1')
    assert len(calls)==1
