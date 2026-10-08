import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError


def assert_code(code, action):
    with pytest.raises(DomainError) as caught:
        action()
    assert caught.value.code == code

from app.support.types import money

from app.domain.merchant import Merchant

@pytest.mark.parametrize("state,action,target", [('ACTIVE', 'activate', None), ('ACTIVE', 'close', 'CLOSED'), ('ACTIVE', 'suspend', 'SUSPENDED'), ('SUSPENDED', 'activate', 'ACTIVE'), ('SUSPENDED', 'close', 'CLOSED'), ('SUSPENDED', 'suspend', None), ('CLOSED', 'activate', None), ('CLOSED', 'close', None), ('CLOSED', 'suspend', None)])
def test_review_transition_table_and_atomic_refusal(state, action, target):
    item = Merchant("M1", "Coffee", "RESTAURANT", "NL")
    paths = {'ACTIVE': (), 'SUSPENDED': ('suspend',), 'CLOSED': ('close',)}
    for setup in paths[state]:
        getattr(item, setup)()
    before = api.view(item)
    if target is None:
        assert_code("INVALID_STATE", lambda: getattr(item, action)())
        assert api.view(item) == before
    else:
        getattr(item, action)()
        assert item.status == target
