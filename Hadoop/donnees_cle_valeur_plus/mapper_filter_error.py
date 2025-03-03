#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    # Assume the severity level is the third token (index 2)
    if len(parts) < 3:
        continue
    severity = parts[2]
    if severity == "ERROR":
        print(line)
