import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    if len(parts) < 2:
        continue
    key = parts[0]
    try:
        value = float(parts[1])
    except ValueError:
        continue
    # Emit key and a pair "value,count" (initial count = 1)
    print(f"{key}\t{value},1")
