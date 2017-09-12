import os
import inspect
from datetime import datetime, timedelta

COLOR_PALETTE = ["#e6194b","#3cb44b","#ffe119","#0082c8",
                 "#f58231","#911eb4","#46f0f0","#f032e6",
                 "#d2f53c","#fabebe","#008080","#e6beff",
                 "#aa6e28","#fffac8","#800000","#aaffc3",
                 "#808000","#ffd8b1","#000080","#808080",
                 "#FFFFFF","#000000"]

DISTANCE_TYPES = [
    # Atom based
    "a:Hamming",
    # String based
    "s:Levenshtein",
    "s:Longest Common Substring",
    "s:Longest Common Subsequence",
    "s:Jaccard",
    "s:Weighted Jaccard",
    "s:Categoric",
    "s:Soundex",
    # Numeric based
    "n:MAPE",
    "n:Normalized MAPE"
]

def listextension(iterableX, iterableY):
    iterableX.extend(iterableY)
    return iterableX

class DatePart(object):
    Days = "D"
    Weeks = "W"
    Months = "M"
    Years = "Y"

    @staticmethod
    def get_days(start, end):
        delta = (end - start).days
        return [start + timedelta(days = day) for day in range(delta + 1)]

    @staticmethod
    def get_weeks(start, end):
        delta_days = (end - start).days
        delta_weeks = delta_days // 7 + (delta_days % 7 > 0)
        return [start + timedelta(weeks = week) for week in range(delta_weeks + 1)]

    @staticmethod
    def get_months(start, end):
        delta_days = (end - start).days
        delta_months = delta_days // 30 + (delta_days % 30 > 0)
        return [start + timedelta(days = month * 30) for month in range(delta_months + 1)]

    @staticmethod
    def get_years(start, end):
        delta_days = (end - start).days
        delta_years = delta_days // 365 + (delta_days % 365 > 0)
        return [start + timedelta(days = year * 365) for year in range(delta_years + 1)]

    @staticmethod
    def get_custom_split(start, end, n_split):
        delta_days = (end - start).days
        delta_split = delta_days // n_split + (delta_days % n_split > 0)
        return [start + timedelta(days = delta_split * split) for split in range(n_split + 1)]

    PARTITIONERS = {
        "D": get_days.__func__,
        "W": get_weeks.__func__,
        "M": get_months.__func__,
        "Y": get_years.__func__,
    }

    @staticmethod
    def get_date_partitions(start, end, datepart):
        if datepart not in DatePart.PARTITIONERS:
            return DatePart.get_custom_split(start, end, datepart)
        return DatePart.PARTITIONERS[datepart](start, end)


class Directory(object):
    def __init__(self, file):
        self.path = os.path.dirname(os.path.realpath(file))
        self.__filename__ = file

    @classmethod
    def current(cls):
        calling_stack = inspect.stack()[1]
        calling_file = calling_stack[1]
        return cls(calling_file)

    def moveup(self):
        self.path = os.path.dirname(self.path)
        return self

    def enter(self, folder):
        self.path = os.path.join(self.path, folder)
        return self

    def __str__(self):
        return self.path
