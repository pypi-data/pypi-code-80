import pytest
from redis.exceptions import ResponseError
from limeutils import byte_conv, ValidationError       # noqa
from icecream import ic     # noqa



param = ['abc', 123, 12.5, 0, 'foo', 'foo', '']
@pytest.mark.parametrize('k', param)
# @pytest.mark.focus
def test_set(red, k):
    assert red.set('sam', k)
    assert red.get('sam') == k
    

# @pytest.mark.focus
def test_list(red):
    red.delete(red.formatkey('many'))
    red.set('many', ['a'])
    red.set('many', ['b'])
    red.set('many', ['c'], insert='start')
    red.set('many', ['d'], insert='start')
    assert red.llen(red.formatkey('many')) == 4
    assert (red.get('many')) == ['d', 'c', 'a', 'b']
    red.set('many', ['foo', 'bar'])
    assert red.llen(red.formatkey('many')) == 6
    assert (red.get('many')) == ['d', 'c', 'a', 'b', 'foo', 'bar']
    red.set('many', ['', 'meh'])
    assert red.llen(red.formatkey('many')) == 8
    assert (red.get('many')) == ['d', 'c', 'a', 'b', 'foo', 'bar', '', 'meh']


# @pytest.mark.focus
def test_hash(red):
    red.delete(red.formatkey('user'))
    red.set('user', dict(age=34, username='enchance', gender='m'))
    assert red.get('user') == dict(age=34, username='enchance', gender='m')
    assert red.get('user', only='username') == dict(username='enchance')
    assert red.get('user', only=['age', 'gender']) == dict(age=34, gender='m')


# @pytest.mark.focus
def test_set_data(red):
    red.delete(red.formatkey('norepeat'))
    red.set('norepeat', {'b', 'a', 'c', 'd', 'a'})
    assert red.get('norepeat') == {'d', 'a', 'b', 'c'}   # unordered of course


param = [
    ('one', 432.5, ['one'], 1), ('two', ['b'], ['one', 'two'], 2),
    ('three', dict(age=34, username='sally', gender='f'), ['one', 'two', 'three'], 3)
]
@pytest.mark.parametrize('key, val, check, out', param)
@pytest.mark.focus
def test_exists(red, key, val, check, out):
    red.set(key, val)
    assert red.exists(*check) == out
    assert isinstance(out, int)
    

# @pytest.mark.focus
def test_overwrite(red, nooverwrite):
    assert red.set('a', 'a')
    assert red.set('a', 1)
    assert red.set('a', 12.5)
    assert red.set('a', [12, 56])
    assert red.set('a', dict(foo='bar'))
    
    with pytest.raises(ResponseError):
        nooverwrite.set('a', [1])
    



# @pytest.mark.focus
def test_exception(red):
    with pytest.raises(ValidationError):
        red.set('fail', ['a', 'b'], insert='foo')
        
    try:
        raise ValidationError(choices=['a', 'b'])
    except ValidationError as e:
        assert e.message == 'Arguments can only be: a or b.'
        # ic(e.message)

    try:
        raise ValidationError(choices=['a', 'b', 'c'])
    except ValidationError as e:
        assert e.message == 'Arguments can only be: a, b, or c.'
        # ic(e.message)

    try:
        raise ValidationError(choices=['a'])
    except ValidationError as e:
        assert e.message == 'Arguments can only be: a.'
        # ic(e.message)

    try:
        raise ValidationError('This is it.')
    except ValidationError as e:
        assert e.message == 'This is it.'
        # ic(e.message)
    