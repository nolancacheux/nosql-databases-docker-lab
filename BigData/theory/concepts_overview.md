# Big Data, ETL, NoSQL, Architectures distribuées et Traitement analytique

## Introduction : Big Data et Motivations

Le Big Data concerne la gestion et l'exploitation de volumes gigantesques de données, hétérogènes, générées rapidement et constamment, afin d’aider à la prise de décisions.

### Motivation principale :

- Explosion des volumes de données (exemple : radiotélescope Square Kilometre Array = 7 To/seconde).
- Évolution de la gestion verticale (renforcer une seule machine très puissante) vers la gestion horizontale (plusieurs machines standards).

### Facteurs facilitant le Big Data :

- Coût réduit du stockage et des processeurs.
- Disponibilité accrue des données.

## Les Caractéristiques du Big Data (les 4V)

- **Volume** : quantité massive de données.
- **Variété** : données très diverses (texte, vidéo, audio…).
- **Vélocité** : rapidité de génération et traitement des données.
- **Véracité** : qualité variable, nécessité de gestion des erreurs et incohérences.

## Limites des SGBD relationnels (SQL)

### Rappel sur SQL :

- Fonctionnement basé sur des jointures entre tables.
- Contraintes ACID :
    - **Atomicité** : tout ou rien.
    - **Cohérence** : validité permanente des données.
    - **Isolation** : indépendance entre transactions.
    - **Durabilité** : persistance des transactions.

### Limites rencontrées :

- Rigidité du schéma relationnel.
- Difficulté à gérer la montée en charge horizontale.
- Coût important du maintien des propriétés ACID à grande échelle.
- Complexité lors de modifications du schéma (impact toutes les applications utilisant ces données).

## Bases de Données NoSQL (Not Only SQL)

Face aux limites du SQL, les bases NoSQL offrent :

- Flexibilité du schéma.
- Adaptées au Big Data grâce au partitionnement (sharding) et à la réplication.

### Catégories de bases NoSQL :

- **Clé-Valeur (Key-Value)** :
    - Exemple : Redis, Amazon DynamoDB
    - Clé : identifiant unique (ex : user:1001)
    - Valeur : simple ou complexe (objet sérialisé JSON)

- **Orientées Colonnes** :
    - Exemple : Cassandra, HBase
    - Stockage par colonnes au lieu de lignes
    - Exemple d’identifiant : Clé primaire user_id=12345, colonnes : nom, âge, adresse.

- **Orientées Documents** :
    - Exemple : MongoDB, CouchDB
    - Stockage sous forme de documents (JSON/BSON)
    - Exemple : { "_id": 1001, "nom": "Alice", "age": 30 }

- **Orientées Graphes** :
    - Exemple : Neo4j
    - Modélisation sous forme de nœuds et de relations (ex : réseaux sociaux, itinéraires)

## Architecture de Distribution (Clustering)

- **Sharding** : Répartition automatique des données sur plusieurs machines.
- **Réplication** : Duplication des données sur plusieurs serveurs pour assurer la disponibilité.

### Réplication maître-esclave (Master-Slave) :

- Maître : lecture/écriture, Esclaves : lecture uniquement.
- Exemple : HBase (Apache), centralisation des écritures.

### Réplication Peer-to-Peer (P2P) :

- Aucune hiérarchie (pas de maître).
- Chaque nœud peut lire/écrire. Protocole Gossip pour synchronisation.
- Exemple : Cassandra (Apache), architecture en anneau, chaque nœud communique avec tous les autres.

## Comparaison HBase, Cassandra, MongoDB

| Caractéristiques | HBase | Cassandra | MongoDB |
|------------------|-------|-----------|---------|
| **Architecture** | Master-Slave | Peer-to-Peer (Ring) | Master-Slave avec Sharding |
| **Modèle** | Colonnes | Colonnes | Documents (JSON) |
| **Évolutivité** | Horizontale élevée | Très haute évolutivité horizontale | Évolutivité horizontale facile |
| **Cohérence** | Forte | Ajustable (généralement éventuelle) | Forte par défaut, configurable |
| **Cas d'usage typique** | Analytique (Hadoop) | Opérationnel, rapide, très grande volumétrie | Flexibilité d’applications web |

## Théorème de CAP (Brewer)

Impossible d'obtenir simultanément :

- **Consistance (Consistency)** : Données identiques sur tous les nœuds.
- **Disponibilité (Availability)** : Système toujours accessible.
- **Tolérance au partitionnement (Partition Tolerance)** : Fonctionnement même en cas de séparation réseau.

Un système distribué ne peut choisir que deux propriétés simultanément.

## Traitement Analytique : Batch vs Temps réel

### Batch Processing (Traitement par lots)

- Hadoop (HDFS, MapReduce)
- Exemple de bases : HBase, MongoDB
- Traitement massif mais différé des données (ex : analyses journalières).

### Real-time Processing (Traitement en temps réel)

- Apache Spark (Streaming), Apache Storm
- Traitement instantané, analyse en continu (ex : monitoring temps réel, Twitter).

## ETL (Extract Transform Load)

Processus d'extraction des données brutes (Extract), leur transformation pour les adapter à un besoin spécifique (Transform), et leur chargement dans un Data Warehouse ou Data Lake (Load).

- Exemple : Charger les données transactionnelles MySQL vers HBase ou Cassandra après transformation via Spark.

## Star Schema vs Snowflake Schema

- **Star Schema** :
    - Schéma de tables dimensionnelles (dimensions) autour d'une table centrale (faits). Facile à interroger, performant pour l'analytique.

- **Snowflake Schema** :
    - Variante du star schema avec dimensions normalisées en plusieurs tables. Plus complexe mais optimise l’espace.
    Il existe principalement deux grandes architectures dans le traitement du Big Data :

### Architecture Lambda (Lambda Architecture)

https://github.com/apssouza22/big-data-pipeline-lambda-arch

L’architecture Lambda combine deux approches distinctes pour gérer les flux de données massifs :

#### Batch layer (Couche Batch)

**Objectif :**
Traiter des données historiques (stockées durablement).

**Exemples d’outils utilisés :**

- Hadoop HDFS (stockage)
- Apache HBase, MongoDB (stockage analytique)
- Apache Hive (requêtage analytique)
- Apache Spark (traitement par lot / batch)

**Caractéristiques :**

- Traitement massif des données
- Lent mais très fiable et précis
- Traitement régulier (toutes les heures/jours/semaines)
- Permet des calculs précis, des agrégations lourdes, et des traitements complexes

#### Speed layer (Couche Temps Réel)

**Objectif :**
Traiter des données en temps réel pour une réponse immédiate.

**Exemples d’outils utilisés :**

- Apache Spark Streaming
- Apache Storm
- Apache Kafka (ingestion rapide de données)

**Caractéristiques :**

- Très rapide (millisecondes ou secondes)
- Permet de fournir des résultats instantanés
- Peut manquer temporairement de précision, mais offre une très faible latence

#### Serving Layer (Couche de Service)

Combine les résultats des couches Batch et Speed pour fournir une réponse unifiée et cohérente aux requêtes utilisateurs.

**Outils typiques :** Cassandra, HBase, Elasticsearch

### Architecture Kappa (Kappa Architecture)

L’architecture Kappa est une simplification de l’architecture Lambda. Elle utilise uniquement la couche temps réel, supprimant la distinction entre batch et streaming.

**Principe :**

- Un seul pipeline (flux) de traitement en temps réel
- Toutes les données historiques et récentes passent par la même couche temps réel
- Les données sont traitées immédiatement au moment où elles arrivent

**Exemples d’outils utilisés :**

- Apache Kafka (stockage des flux)
- Apache Flink ou Apache Spark Streaming (traitement temps réel)

**Avantages :**

- Moins complexe (pas de gestion séparée des couches batch et temps réel)
- Plus facile à maintenir et faire évoluer
- Idéale pour les traitements qui exigent une faible latence constante

**Inconvénients :**

- Complexité accrue pour rejouer des données anciennes (nécessité de stocker tout l’historique dans Kafka ou système équivalent)
- Difficulté accrue pour les traitements analytiques très complexes nécessitant des recalculs réguliers sur de gros volumes historiques

### Comparatif résumé des deux architectures :

| Aspect                  | Architecture Lambda               | Architecture Kappa                |
|-------------------------|-----------------------------------|-----------------------------------|
| **Complexité**          | Élevée (2 couches distinctes)     | Plus faible (1 seule couche)      |
| **Performance**         | Latence variable selon la couche  | Faible latence constante          |
| **Facilité de gestion** | Plus complexe à maintenir         | Plus facile à gérer               |
| **Traitements historiques** | Très performants (batch)     | Complexes (nécessité de rejouer tout le flux) |
| **Exemples d’usage**    | Traitement analytique complexe + temps réel | Temps réel permanent |

### Exemple de cas typique :

- **Lambda :**
    - Traitement financier (historique précis + transactions temps réel)

- **Kappa :**
    - Analyse de comportement utilisateur en temps réel (ex : réseaux sociaux, streaming vidéo)

## Grands Acteurs du Web et contributions Big Data :

- **Facebook** : Cassandra (2009), HBase et Hive.
- **Google** : GoogleFS, MapReduce, BigTable.
- **Amazon** : DynamoDB (Key-Value, architecture peer-to-peer).

## Real-time Monitoring

Surveillance continue de données opérationnelles.

- Exemple : Grafana connecté à Cassandra ou Spark Streaming pour afficher instantanément des métriques.

## Conclusion et Outils vus :

- Hadoop (stockage et traitement distribué).
- Cassandra (peer-to-peer, haute disponibilité).
- HBase (analytique, Master-Slave).
- MongoDB (documents flexibles, facile à développer).
- Spark Streaming (traitement temps réel puissant).
- ETL (MySQL vers systèmes Big Data).