#!encoding=utf-8
import unittest
from ivystar.src.decorator import timer
from ivystar.src.decorator import prilog

class TestSetUp(unittest.TestCase):

    def setUp(self):
        print(">>> start test")


    def test_run(self):

        @log
        def fast(x, y):
            return x*y
        fast(3,5)

        @timer
        def fast(x, y):
            return x*y
        fast(3,5)

        @run_every(1, "second")
        def test_run_test():
            print("hello world")

    def tearDown(self):
        print("<<< test end")

if __name__ == "__main__":
    unittest.main()
else:
    unittest.main()
