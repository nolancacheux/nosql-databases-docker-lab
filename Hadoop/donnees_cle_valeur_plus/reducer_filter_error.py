#!/usr/bin/env python3
import sys

for line in sys.stdin:
    print(line.strip())

#strip removes leading and trailing whitespaces
#example: "  hello world  ".strip() returns "hello world"