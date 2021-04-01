import pandas as pd
from test_data import test_data
from __init__ import SpectroscopyAnalysis
import unittest
import pdb

class TestSetUp(unittest.TestCase):
    # 前置条件当中
    # 每一个测试用例方法执行之前都会运行的代码
    # 可以把测试数据放到 setUp 当中

    def setUp(self):
        print(test_data[:3])
        self.data = [[float(j) for j in i.split(",")] for i in test_data]
        print("\n===start test\n")

    def test_run(self):
        sa = SpectroscopyAnalysis()
        assert(type(sa.spectrum(self.data)) == tuple)
        assert(type(sa.envelope(self.data)) == tuple)
        assert(type(sa.power(self.data)) == tuple)

    def tearDown(self):
        print("\n===end test\n")

if __name__ == "__main__":
    unittest.main()
else:
    unittest.main()


