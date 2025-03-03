
import sys

current_key = None
total_sum = 0
total_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    key, val_count = line.split('\t', 1)
    try:
        value_str, count_str = val_count.split(',')
        value = float(value_str)
        count = int(count_str)
    except ValueError:
        continue

    if current_key == key:
        total_sum += value
        total_count += count
    else:
        if current_key is not None:
            avg = total_sum / total_count if total_count != 0 else 0
            print(f"{current_key}\t{avg}")
        current_key = key
        total_sum = value
        total_count = count

if current_key is not None:
    avg = total_sum / total_count if total_count != 0 else 0
    print(f"{current_key}\t{avg}")
