import os
import sys
import unittest

# 将项目根目录添加到 sys.path 中, 从而可以直接调用对应 file、module 里的全局函数
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BaseFunctions.Commons import Commons
from vcmain import main

class TestCheckForSpace(unittest.TestCase):

    def test_check_for_space_normal(self):
        path = "test path"
        expected = "test\\ path"
        result =  main.check_for_space(path)
        self.assertEqual(result, expected)

    def test_check_for_space_combined(self):
        path = "test path (with spaces)"
        expected = "test\\ path\\ \\(with\\ spaces\\)"
        result = main.check_for_space(path)
        self.assertEqual(result, expected)
        
    def test_check_for_space2_normal(self):
        path = "test path"
        expected = main.check_for_space(path)
        result =  Commons.check_for_space(path)
        self.assertEqual(result, expected)

    def test_check_for_space2_combined(self):
        path = "test path (with spaces)"
        expected = main.check_for_space(path)
        result = Commons.check_for_space(path)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
