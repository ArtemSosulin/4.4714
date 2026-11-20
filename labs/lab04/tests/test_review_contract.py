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

from app.domain.acceptance import RestrictedCategoryRule, AcceptedChannelRule

from app.support.types import MerchantContext

def test_review_empty_deny_set_is_not_empty_allow_set():
    item = Merchant("M", "Casino", "GAMBLING", "NL")
    assert RestrictedCategoryRule(set()).check(item, MerchantContext()).allowed
    assert not AcceptedChannelRule(set()).check(item, MerchantContext()).allowed
    values = {"POS"}
    rule = AcceptedChannelRule(values)
    values.clear()
    assert rule.check(item, MerchantContext()).allowed
    assert rule.check(item, MerchantContext("ONLINE")).code == "MERCHANT_CHANNEL_DENIED"
