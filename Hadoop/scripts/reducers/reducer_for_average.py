
import sys

current_key = None
value_sum = 0
count = 0

for line in sys.stdin:
    # Nettoyage de la ligne et séparation
    line = line.strip()
    key, value = line.split('  ')
    
    try:
        value = float(value)
    except ValueError:
        continue
    
    # Si on change de clé (et que ce n'est pas la première ligne)
    if current_key == key:
        value_sum += value
        count += 1
    else:
        # Si ce n'est pas la première ligne, on affiche la moyenne de la clé précédente
        if current_key is not None:
            print("%s %s"% (current_key,value_sum / count))
        current_key = key
        value_sum = value
        count = 1

# N'oubliez pas d'imprimer la dernière clé
if current_key == key:
    print("%s %s"% (current_key,value_sum / count))
