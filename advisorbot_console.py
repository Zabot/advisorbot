#!/bin/env python

import sys
import question_handler

while not False:
    line = sys.stdin.readline()
    response = question_handler.handle(line)
    print(response)

