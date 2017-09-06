# -*- coding: utf-8 -*-

import random


def increase_student_number_randomly(current, step, min, max):
    """
    @ 随机的增加学生人数
    :param current: 当前人数
    :param step: 增加的步长
    :param min: 最小值
    :param max: 最大值
    :return: 1. 如果当前值小于最小值, 返回最小值;
             2. 如果增加之后的值大于最大值, 返回最大值
    """
    assert isinstance(current, (int, long))
    assert isinstance(step, (int, long))
    assert isinstance(min, (int, long))
    assert isinstance(max, (int, long))
    if current < min:
        return min
    if current >= max:
        return max
    current += random.randint(0, step)
    if current >= max:
        return max
    return current
