import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    if len(parts) < 2:
        continue
    city = parts[0]
    try:
        temp = float(parts[1])
    except ValueError:
        continue
    # Emit city and temperature
    print(f"{city}\t{temp}")
