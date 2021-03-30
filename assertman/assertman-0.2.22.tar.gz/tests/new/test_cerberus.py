from assertman.assert_that import that
from assertman.matchers import *


def test_dict():

    assert that({"name": "qwerty", "age": 15}).should(has_entries(name="q werty"))