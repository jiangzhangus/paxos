# Challenge #3 - Programming
# You are given a string composed of only 1s, 0s, and Xs.
#
# Write a program that will print out every possible combination where you replace the X with both 0 and 1.
#
# Some examples:
#
# $ myprogram X0
# 00
# 10
#
# $ myprogram 10X10X0
# 1001000
# 1001010
# 1011000
# 1011010
#
# While your program will take longer to run based on the number of combinations you output, your program shouldn’t crash (or hang) on an input with many Xs.
#
# What is the big O notation for this program?


class Solution:


    def __init__(self, str_input):
        self.segments = str_input.split('X')


    def test_simple(self):
        input = 'x0'
        for result in self.__get_next_result():
            assert result in ('00', '10')

    def test_rightX(self):
        input = '1x'
        for result in self.__get_next_result():
            assert result in ('10', '11')

    def __get_next_result(self):
        yield [0,1]

    def show_all(self):
        for item in self.__get_next_result():
            print(item)