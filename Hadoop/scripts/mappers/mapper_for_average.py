
import sys

for line in sys.stdin:
    # Nettoyage de la ligne et séparation par espace
    line = line.strip()
    key, value = line.split()
    # Émission de la clé et de la valeur
    print("%s  %s"% (key,value))