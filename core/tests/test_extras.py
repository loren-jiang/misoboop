import pytest
from core.templatetags import core_extras

def test_url_replace(rf):
    request = rf.get('/')
    url_replaced = core_extras.url_replace(request, 'test', [1,2,3])
    assert url_replaced == "test=%5B1%2C+2%2C+3%5D"

def test_min_to_hr():
    case_1 = core_extras.min_to_hr('90')
    assert case_1 == '1hr 30min'

    case_2 = core_extras.min_to_hr('45')
    assert case_2 == '45min'

    case_3 = core_extras.min_to_hr('120')
    assert case_3 == '2hr'

def test_get_item():
    d = {'key': 'test'}
    case_1 = core_extras.get_item(d, 'key')
    assert case_1 == 'test'

def test_get_obj_item():
    class A:
        count = 1
    a = A()
    assert core_extras.get_obj_item(A, 'count') == 1

def test_create_list():
    assert core_extras.create_list(1,2,3) == (1,2,3)

def test_split():
    assert core_extras.split('be.boop', '.') == ['be', 'boop']
