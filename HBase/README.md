# Cours et TP détaillé sur HBase

## Introduction à HBase

**HBase** est un système de gestion de bases de données distribuées, non relationnel, orienté colonnes. Développé en Java, il est conçu pour gérer de grandes quantités de données structurées en tables volumineuses. Basé sur une architecture maître/esclave, il permet une scalabilité horizontale efficace.

HBase s'intègre généralement à l'écosystème Hadoop, utilisant HDFS pour le stockage distribué.


---


## Comparaison : HBase vs Cassandra vs MongoDB

Ces trois bases de données NoSQL sont adaptées au traitement de grandes quantités de données, mais se distinguent par leur modèle de données, architecture et cas d'utilisation :

### Tableau comparatif

| **Caractéristique**        | **HBase**                                  | **Cassandra**                              | **MongoDB**                                |
|----------------------------|--------------------------------------------|--------------------------------------------|--------------------------------------------|
| **Type**                   | Colonnes distribuées                       | Colonnes distribuées                       | Documents JSON                             |
| **Modèle de données**      | Colonnes (comme Bigtable)                  | Colonnes avec clé-partition                | Documents JSON (BSON)                      |
| **Scalabilité**            | Horizontale (dépend d'Hadoop)              | Horizontale (décentralisée)                | Horizontale avec Sharding                  |
| **Architecture**           | Basée sur Hadoop HDFS et Zookeeper         | Peer-to-peer                               | Maître-esclave (Replica Sets & Sharding)   |
| **Lecture**                | Optimisée pour les lectures séquentielles  | Rapide (aléatoire)                         | Rapide (recherches complexes et indexées)  |
| **Écriture**               | Massives                                   | Très rapide                                | Bonne (peut ralentir avec index complexes) |
| **Tolérance aux pannes**   | Dépend d’HDFS                              | Très robuste (aucun SPOF)                  | Bonne (Replica Set maître requis)          |
| **Cas d’utilisation**      | Logs massifs, analytique Big Data          | IoT, télécoms, transactions bancaires      | Web, catalogues produits, contenu flexible |

### Quand utiliser ?

- **HBase** : Big Data, analyse massive, intégration Hadoop.
- **Cassandra** : Haute disponibilité, transactions rapides.
- **MongoDB** : Flexibilité JSON, web, gestion de contenu.

## Installation et Configuration avec Docker

### 1. Création des conteneurs Docker

Exécuter les commandes suivantes pour lancer les conteneurs :

```bash
docker run -itd --net=hadoop -p 50070:50070 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/hadoop-cluster:latest

docker run -itd -p 8040:8042 --net=hadoop --name hadoop-worker1 --hostname hadoop-worker1 liliasfaxi/hadoop-cluster:latest

docker run -itd -p 8041:8042 --net=hadoop --name hadoop-worker2 --hostname hadoop-worker2 liliasfaxi/hadoop-cluster:latest
```

Vérifier les conteneurs actifs :

```bash
docker ps
```

### 2. Configuration HBase

Entrer dans le conteneur `hadoop-master` :

```bash
docker exec -it hadoop-master bash
```

Arrêter tous les services Hadoop (au cas où ils tournent déjà) :

```bash
stop-all.sh
jps
```

Aller dans le dossier de configuration HBase :

```bash
cd $HBASE_HOME/conf/
```

Modifier le fichier `hbase-site.xml` avec `vim` :

```bash
vim hbase-site.xml
# Appuyer sur i pour modifier
# Remplacer localhost par hadoop-master, hadoop-worker1, hadoop-worker2
# CTRL+C puis :wqa pour enregistrer et quitter
```

Modifier également le fichier `regionservers` :

```bash
vim regionservers
# Appuyer sur i pour modifier
# Remplacer localhost par hadoop-worker1, hadoop-worker2
# CTRL+C puis :wqa pour enregistrer et quitter
```

### 3. Démarrage des services Hadoop et Kafka/Zookeeper

Revenir au dossier principal et démarrer Hadoop puis Kafka/Zookeeper :

```bash
cd
./start-hadoop.sh
./start-kafka-zookeeper.sh


# if it doesn't work, try with option
# jps 
# kill number of process that are not needed
#  docker stop hadoop-master
#  docker start hadoop-master
#  docker exec -it hadoop-master bash
#  ./start-hadoop.sh
#  ./start-kafka-zookeeper.sh


```


### 4. Démarrage de HBase

Ouvrir un nouveau terminal, entrer à nouveau dans le conteneur `hadoop-master`, puis démarrer HBase :

```bash
docker exec -it hadoop-master bash
start-hbase.sh
hbase shell
```

Vérifications finales dans HBase :

```bash
whoami
version
status
```

---


---

## TP HBase : Exercices pratiques

**Important** : Une fois créées, les familles de colonnes ne peuvent plus être supprimées facilement.

### Exercice étape par étape

1. **Lister le nombre de serveurs HBase :**
   ```
   status
```

2. **Créer une table HBase**
```bash
create 'customer', 'address', 'order'
```

2.1. **Vérification :**

```bash
list
```

2. **Afficher contenu de la table** :

```bash
scan 'customer'
```

3. **Désactiver la table** :

```bash
disable 'customer'
```

4. **Afficher une table désactivée (test)** :

```bash
scan 'customer' # Erreur attendue
```

5. **Réactiver la table** :

```bash
enable 'customer'
```

5. **Ajouter une famille de colonne** :

```bash
alter 'customer', {NAME=>'personal data'}
```

6. **Supprimer une famille de colonne** :

```bash
alter 'customer', 'delete'=>'personal data'
```

7. **Ajouter des données clients** :

```bash
put 'customer', '1', 'address:city','Paris'
put 'customer', '1', 'address:state','France'
put 'customer', '1', 'address:street','Rue 1'
scan 'customer'
```

8. **Ajouter un second client** :

```bash
put 'customer', '2', 'address:city','Nancy'
put 'customer', '2', 'address:state','France'
put 'customer', '2', 'address:street','Rue centrale'
```

9. **Lecture sélective des données** :

```bash
get 'customer', '1', {COLUMN=>'address:city'}
scan 'customer', {COLUMNS=>['address:city']}
```

10. **Suppression des données spécifiques** :

```bash
delete 'customer', '1', 'address:city'
deleteall 'customer', '2'
```

10. **Historique des versions de colonne** :

```bash
alter 'customer',{NAME=>'address', VERSIONS=>3}
put 'customer', '1', 'address:city','Paris'
put 'customer', '1', 'address:city','Lyon'
put 'customer', '1', 'address:city','Lyon'
scan 'customer',{COLUMN=>'address:city', VERSIONS=>2}
```

11. **Supprimer une table (désactiver avant suppression)** :

```bash
disable 'customer'
drop 'customer'
```

---

### Commandes utiles en résumé :

- `status`: affiche l'état des serveurs HBase
- `version`: version actuelle d'HBase
- `whoami`: utilisateur actif
- `list`: liste les tables
- `create`: crée une nouvelle table
- `scan`: affiche le contenu
- `disable`: désactive une table
- `enable`: réactive une table
- `alter`: modifie une table (ajout/suppression de colonnes)
- `delete/deleteall`: supprime des entrées
- `drop`: supprime une table (désactivée avant)

---

# TP2 : Exercices pratiques sur HBase

## Exercice 1 : Table « Projet »

1. Créer la table « Projet » avec les familles de colonnes nécessaires :
    ```bash
    create 'Projet', 'Infos', 'Details'
    ```

2. Ajouter une famille de colonnes « DateFin » :
    ```bash
    alter 'Projet', {NAME=>'DateFin'}
    ```

3. Insérer les données dans la table « Projet » :
    ```bash
    # Projet Proj1
    put 'Projet', 'Proj1', 'Infos:Nom', 'Analyse Big Data'
    put 'Projet', 'Proj1', 'Infos:Ville', 'Lille'
    put 'Projet', 'Proj1', 'Details:DateLancement', '2024-01-10'
    put 'Projet', 'Proj1', 'DateFin:Prevue', '2024-06-15'

    # Projet Proj2
    put 'Projet', 'Proj2', 'Infos:Nom', 'Développement Web'
    put 'Projet', 'Proj2', 'Infos:Ville', 'Lyon'
    put 'Projet', 'Proj2', 'Details:DateLancement', '2023-12-01'
    put 'Projet', 'Proj2', 'DateFin:Prevue', '2024-05-20'

    # Projet Proj3
    put 'Projet', 'Proj3', 'Infos:Nom', 'Machine Learning'
    put 'Projet', 'Proj3', 'Infos:Ville', 'Marseille'
    put 'Projet', 'Proj3', 'Details:DateLancement', '2024-02-15'
    put 'Projet', 'Proj3', 'DateFin:Prevue', '2024-08-01'
    ```

4. Mettre à jour la ville du projet « Proj3 » à Paris :
    ```bash
    put 'Projet', 'Proj3', 'Infos:Ville', 'Paris'
    ```

5. Afficher les données de la table :
    ```bash
    scan 'Projet'
    ```

6. Afficher la date de lancement du projet « Proj2 » :
    ```bash
    get 'Projet', 'Proj2', {COLUMN=>'Details:DateLancement'}
    ```

## Exercice 2 : Table « rainforest »

1. Créer la table « rainforest » avec deux familles : recordings, duration :
    ```bash
    create 'rainforest', 'recordings', 'duration'
    ```

2. Ajouter une famille de colonnes « year » à la table :
    ```bash
    alter 'rainforest', {NAME=>'year'}
    ```

3. Insérer les données dans la table :
    ```bash
    # Enregistrement Jude
    put 'rainforest', '1', 'recordings:Title', 'Jude'
    put 'rainforest', '1', 'recordings:Artist', 'Courteeners'
    put 'rainforest', '1', 'recordings:Price', '7.99'
    put 'rainforest', '1', 'duration:length', '15'
    put 'rainforest', '1', 'year:release', '2020'

    # Enregistrement Symphony No 5
    put 'rainforest', '2', 'recordings:Title', 'Symphony No 5'
    put 'rainforest', '2', 'recordings:Artist', 'Tchaikovsky'
    put 'rainforest', '2', 'recordings:Price', '8.75'
    put 'rainforest', '2', 'duration:length', '10'
    put 'rainforest', '2', 'year:release', '2021'

    # Enregistrement Jazz
    put 'rainforest', '3', 'recordings:Title', 'Jazz'
    put 'rainforest', '3', 'recordings:Artist', 'James Brown'
    put 'rainforest', '3', 'recordings:Price', '6.99'
    put 'rainforest', '3', 'duration:length', '9'
    put 'rainforest', '3', 'year:release', '2020'
    ```

4. Afficher toutes les données de la table :
    ```bash
    scan 'rainforest'
    ```

5. Afficher les enregistrements dont le prix (Price) est 6.99 :
    ```bash
    scan 'rainforest', {FILTER => "SingleColumnValueFilter('recordings', 'Price', =, 'binary:6.99')"}
    ```

6. Afficher les enregistrements de l'année 2020 :
    ```bash
    scan 'rainforest', {FILTER => "SingleColumnValueFilter('year', 'release', =, 'binary:2020')"}
    ```

7. Mettre à jour la durée (Duration) de l’enregistrement « Jazz » à 12 :
    ```bash
    put 'rainforest', '3', 'duration:length', '12'
    ```

8. Afficher les données après mise à jour pour vérifier :
    ```bash
    get 'rainforest', '3'
    ```

9. Afficher toutes les données de la table pour vérification :
    ```bash
    scan 'rainforest'
    ```

## Résumé

| Commande | Utilité |
| --- | --- |
| `create 'table','famille1', ...` | Crée une nouvelle table |
| `put` | Ajoute ou modifie une entrée |
| `scan` | Affiche toutes les données d'une table |
| `get` | Affiche une ligne spécifique |
| `alter` | Ajoute/modifie une famille de colonnes |
| `disable & drop` | Désactive puis supprime une table |
| `SingleColumnValueFilter` | Filtre une table selon une valeur de colonne |
