#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    # Si le niveau se trouve par exemple en 4ème position, modifiez ici
    # Pour l'instant, on suppose toujours qu'il est en position 2
    if len(parts) < 3:
        continue
    severity = parts[2]
    if severity.upper() == "ERROR":
        print(line)
