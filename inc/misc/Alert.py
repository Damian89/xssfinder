#!/usr/bin/env python
# coding: utf8

class Alert:
    RED = '\033[31m'
    ORANGE = '\033[33m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    END = '\033[0m'

    @classmethod
    def error(self):
        return "{}[ERROR]{}     ".format(self.RED, self.END)

    @classmethod
    def warning(self):
        return "{}[WARN]{}      ".format(self.ORANGE, self.END)

    @classmethod
    def success(self):
        return "{}[SUCCESS]{}   ".format(self.GREEN, self.END)

    @classmethod
    def info(self):
        return "{}[INFO]{}      ".format(self.BLUE, self.END)
