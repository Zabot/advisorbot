#!/bin/env python

import sys
import question_handler

print("Any text on stdin while be interpreted as if it was in a message to advisorbot")
print("Ctrl-D to exit")

for line in sys.stdin:
    response = question_handler.handle(line)
    print(response)

