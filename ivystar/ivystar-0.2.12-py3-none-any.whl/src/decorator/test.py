#!encoding=utf-8
import unittest
from ivystar.src.decorator import timer
from ivystar.src.decorator import prilog
from ivystar.src.decorator import run_every

class TestSetUp(unittest.TestCase):

    def setUp(self):
        print(">>> start test")


    def test_run(self):

        @prilog
        def fast(x, y):
            return x*y
        print("print log")
        fast(3,5)

        @timer
        def fast(x, y):
            return x*y
        print("print timer")
        fast(3,5)

        @run_every(1, "second")
        def test_run_test():
            print("hello world")
        #test_run_test()
        print("print run_every")

    def tearDown(self):
        print("<<< test end")

if __name__ == "__main__":
    unittest.main()
else:
    unittest.main()
