import unittest
from ProjectSem2 import *


class TestProjectSem(unittest.TestCase):
    def test_search(self):
        scrh.set('Name')
        entrybox_search.insert(0, 'bishal')

        test_array=[('1','bishal','bidari','20','male','9849208599','bhainsepati'),
                    ('2','Saman','Thapa','19','male','9841261144','bhainsepati')]

        expectedresult=[('1','bishal','bidari','20','male','9849208599','bhainsepati')]
        mylist = search(test_array)
        self.assertEqual(mylist, expectedresult)

    def test_sort(self):
        srt.set('Name')
        array_test = [('1','bishal','bidari','20','male','9849208599','bhainsepati'),
                        ('2','Saman','Thapa','19','male','9841261144','bhainsepati')]
        expected_result = [('1','bishal','bidari','20','male','9849208599','bhainsepati'),
                        ('2','Saman','Thapa','19','male','9841261144','bhainsepati')]

        quick_sort(array_test, 0, len(array_test) - 1)
        self.assertEqual(array_test, expected_result)


if __name__ == '__main__':
    unittest.main()