"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
通用模块
Authors: jdh99 <jdh821@163.com>
"""

import unittest

# IA地址字节数
IA_LEN = 8


def bytes_to_ia(data: bytearray) -> int:
    """从字节流中取出IA地址.字节流是大端"""
    if len(data) < IA_LEN:
        return 0

    ia = 0
    for i in range(IA_LEN):
        ia += data[i] << ((IA_LEN - 1 - i) << 3)
    return ia


def ia_to_bytes(ia: int) -> bytearray:
    """将IA地址转换为字节流.字节流是大端"""
    data = bytearray()
    for i in range(IA_LEN):
        data.append((ia >> ((IA_LEN - 1 - i) << 3)) & 0xff)
    return data


class _UnitTest(unittest.TestCase):
    def test_bytes_to_ia(self):
        ia = bytes_to_ia(bytearray([0x21, 0x40, 0x00, 0x00, 0x00, 0x00, 0x04, 0x01]))
        self.assertEqual(ia, 0x2140000000000401)

    def test_ia_to_bytes(self):
        data = ia_to_bytes(0x2140000000000401)
        self.assertEqual(data, bytearray([0x21, 0x40, 0x00, 0x00, 0x00, 0x00, 0x04, 0x01]))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
