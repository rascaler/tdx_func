import unittest


class ApiTest(unittest.TestCase):
    def setUp(self):
        print("测试用例执行前的初始化操作========")

    def tearDown(self):
        print("测试用例执行完之后的收尾操作=====")

    def test_a(self):
        print(1)
        pass

    def test_b(self):
        print(2222222)
        pass

    def test_b(self):
        print(3333)
        pass