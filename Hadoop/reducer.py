import sys

current_word = None
current_count = 0

# Lire l'entrée depuis stdin (entrée standard)
for line in sys.stdin:
    line = line.strip()  # Supprimer les espaces en début et fin de ligne
    try:
        word, count = line.split("\t", 1)  # Séparer le mot et le nombre
        count = int(count)  # Convertir le nombre en entier
    except ValueError:
        continue  # Ignorer les lignes mal formatées

    # Si c'est le même mot que le précédent, on incrémente son compteur
    if current_word and current_word == word:
        current_count += count
    else:
        # Si c'est un nouveau mot, afficher l'ancien mot avec son total
        if current_word:
            print('%s\t%s' % (current_word, current_count))
        current_word = word  # Définir le nouveau mot
        current_count = count  # Réinitialiser le compteur

# Imprimer le dernier mot et son nombre
if current_word:
    print('%s\t%s' % (current_word, current_count))
