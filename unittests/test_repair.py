import unittest
import sys
from CUTE_components import repair


class TestRepair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n测试开始了")
        print("当前模块所属的包名是：", __package__)

    @classmethod
    def tearDownClass(cls):
        print("测试结束了")

    def test_example1(self):
        self.assertNotEqual(1, 2)

    @unittest.skipIf(sys.version_info < (3, 9), "only support 3.9+")
    def test_example2(self):
        self.assertNotEqual(3, 4)


if __name__ == '__main__':
    unittest.main()
