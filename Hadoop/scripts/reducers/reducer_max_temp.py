import sys

current_city = None
max_temp = None

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    city, temp_str = line.split('\t', 1)
    try:
        temp = float(temp_str)
    except ValueError:
        continue

    if current_city == city:
        if temp > max_temp:
            max_temp = temp
    else:
        if current_city is not None:
            print(f"{current_city}\t{max_temp}")
        current_city = city
        max_temp = temp

if current_city is not None:
    print(f"{current_city}\t{max_temp}")
