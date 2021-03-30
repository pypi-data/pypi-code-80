from assertman.assert_that import that
from assertman.matchers import *
import datetime
from assertman.objects import AssertableDict


def test_int():
    assert that(34).should(equal_to(34))


def test_str():
    assert that("qwerty").should(starts_with("qwe"))


def test_list():
    assert that(['3', '4', '5']).should(has_item('3'))


def test_list_with_filter1():
    assert that([{"name": "qwerty", "age": 15}, {"name": "zxcvb", "age": 45}])\
        .filter(name="qwerty")\
        .should(has_length(1))

    assert that([{"name": "qwerty", "age": 15}, {"name": "zxcvb", "age": 45}]) \
        .filter(name="qwerty") \
        .should(has_item(has_entries(age=15)))


def test_list_with_find():
    assert that([{"name": "qwerty", "age": 15}, {"name": "zxcvb", "age": 45}]) \
        .find(name="qwerty")\
        .should(has_entries(age=15))


def test_custom_list_matchers():
    assert that([4, 5, 6]).should(every_item(greater_than(2)))


def test_dict():
    assert that({"name": "qwerty", "age": 15}).should(has_entries(name="qwerty"))


def test_dict_with_extract():
    assert that({"name": "qwerty", "age": 15})\
        .extract('name')\
        .should(equal_to("qwerty"))


def test_all_in_one():
    assert that({
      "firstName": "John",
      "lastName": "doe",
      "age": 26,
      "address": {
        "streetAddress": "naist street",
        "city": "Nara",
        "postalCode": "630-0192"
      },
      "phoneNumbers": [
        {
          "type": "iPhone",
          "number": "0123-4567-8888"
        },
        {
          "type": "home",
          "number": "0123-4567-8910"
        }
      ]
    }).extract('phoneNumbers')\
        .find(type="iPhone")\
        .should(has_entries(number="0123-4567-8888"))



def test_some_extract():
    obj = that({
      "firstName": "John",
      "lastName": "doe",
      "age": 26,
      "address": {
        "streetAddress": "naist street",
        "city": "Nara",
        "postalCode": "630-0192"
      },
      "phoneNumbers": [
        {
          "type": "iPhone",
          "number": "0123-4567-8888"
        },
        {
          "type": "home",
          "number": "0123-4567-8910"
        }
      ]
    })

    assert obj.should(has_entries(address=has_entries(city="Nara")))
    assert obj.extract('address').should(has_entries(city="Nara"))
    assert obj.should(has_entries(address=has_entries(city="Nara")))

    assert obj.extract('address').extract("streetAddress").should(equal_to("naist street"))
    assert obj.should(has_entries(address=has_entries(city="Nara")))

    assert obj.extract("phoneNumbers").filter(type="iPhone").should(has_length(1))
    assert obj.extract("phoneNumbers").find(type="iPhone").should(has_entries(number="0123-4567-8888"))
    assert obj.extract("phoneNumbers").find(type="home").extract("number").should(equal_to("0123-4567-8910"))


def test_one():
    obj = AssertableDict({
        "streetAddress": "naist street",
        "city": "Nara",
        "postalCode": "630-0192"
      })

    obj.should(has_entries(city="Nara"))