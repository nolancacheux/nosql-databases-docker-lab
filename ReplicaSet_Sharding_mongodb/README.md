# Configuration de MongoDB avec ReplicaSet et Sharding

## 1️⃣ Introduction : Notions Fondamentales en NoSQL

### CAP Theorem

Le théorème CAP stipule qu'un système distribué ne peut garantir simultanément que deux des trois propriétés suivantes :

- **Consistency (C)** : Tous les nœuds voient les mêmes données au même moment.
- **Availability (A)** : Chaque requête reçoit une réponse (succès ou échec).
- **Partition Tolerance (P)** : Le système fonctionne même en cas de perte de connexion ou de panne de certains nœuds.

Dans MongoDB, un ReplicaSet assure la partition tolerance en répliquant les données sur plusieurs instances.

## 2️⃣ Mise en Place d'un ReplicaSet MongoDB avec Docker

Nous utilisons Docker Compose pour simuler un ReplicaSet et un système de sharding.

Docker et Docker Compose installés.

### Docker Compose Configuration

Le fichier `docker-compose.yml` suivant définit :

- Un serveur de configuration (configsvr)
- Deux shards (shard1 et shard2)
- Un routeur (mongos) pour gérer le sharding

```yaml
version: '3.8'

services:
  configsvr:
    image: mongo
    command: ["mongod", "--configsvr", "--replSet", "configReplSet", "--port", "27019", "--bind_ip_all"]
    ports:
      - 27019:27019
    volumes:
      - configdb:/data/db

  shard1:
    image: mongo
    command: ["mongod", "--shardsvr", "--replSet", "sh1", "--port", "27031", "--bind_ip_all"]
    ports:
      - 27031:27031
    volumes:
      - shard1:/data/db

  shard2:
    image: mongo
    command: ["mongod", "--shardsvr", "--replSet", "sh2", "--port", "27032", "--bind_ip_all"]
    ports:
      - 27032:27032
    volumes:
      - shard2:/data/db

  mongos:
    image: mongo
    command: ["mongos", "--configdb", "configReplSet/configsvr:27019", "--port", "27017", "--bind_ip_all"]
    depends_on:
      - configsvr
      - shard1
      - shard2
    ports:
      - 27017:27017

volumes:
  configdb:
  shard1:
  shard2:
```

### Démarrage des Services

Lancer l’environnement :

```sh
docker-compose up -d
```

Vérifier les noms des conteneurs pour les prochaines commandes :

```sh
docker-compose ps
```

## 3️⃣ Initialisation du ReplicaSet (Config Server)

### Initialisation du serveur de configuration

Se connecter au serveur de configuration :

```sh
docker exec -it non_relationnal_database_docker_mongodb-configsvr-1 mongosh --port 27019
```

Initialiser le ReplicaSet :

```javascript
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [
    { _id: 0, host: "configsvr:27019" }
  ]
})
```

Vérifier que le serveur est bien PRIMARY :

```javascript
rs.status()
```

## 4️⃣ Initialisation des Shards

### Vérification et Initialisation des ReplicaSets

Vérifier le nom des hôtes des shards :

```sh
docker exec -it non_relationnal_database_docker_mongodb-shard1-1 hostname
docker exec -it non_relationnal_database_docker_mongodb-shard2-1 hostname
```

Se connecter à chaque shard et les initialiser avec leur nom réel :

#### Shard 1 :

```sh
docker exec -it non_relationnal_database_docker_mongodb-shard1-1 mongosh --port 27031
```

```javascript
rs.initiate({
  _id: "sh1",
  members: [{ _id: 0, host: "107fc119325f:27031" }]
})
```

#### Shard 2 :

```sh
docker exec -it non_relationnal_database_docker_mongodb-shard2-1 mongosh --port 27032
```

```javascript
rs.initiate({
  _id: "sh2",
  members: [{ _id: 0, host: "b96c699ca075:27032" }]
})
```

Vérifier l’état des ReplicaSets :

```javascript
rs.status()
```

## 5️⃣ Ajout des Shards à Mongos

Se connecter au routeur mongos :

```sh
docker exec -it non_relationnal_database_docker_mongodb-mongos-1 mongosh --port 27017
```

Ajouter les shards avec leur nom d’hôte correct :

```javascript
sh.addShard("sh1/107fc119325f:27031")
sh.addShard("sh2/b96c699ca075:27032")
```

Vérifier que les shards sont bien ajoutés :

```javascript
sh.status()
```

## 6️⃣ Activation du Sharding

Activer le sharding sur `testDB` :

```javascript
sh.enableSharding("testDB")
```

Créer une collection et ajouter un index :

```javascript
use testDB
db.createCollection("test")
db.test.createIndex({ "_id": 1 })
```

Sharder la collection :

```javascript
sh.shardCollection("testDB.test", { "_id": 1 })
```

Vérifier la répartition des chunks :

```javascript
sh.status()
```

## 7️⃣ Vérification du Sharding

Importer des données de test :

```sh
mongoimport --db testDB --collection test --file restaurants.json --port 27017
```

Vérifiez que les données ont bien été importées :

```javascript
use testDB
db.test.find().pretty()
```

### Vérification et Répartition des Chunks

Vérifier la distribution actuelle des données :

```javascript
db.test.getShardDistribution()
```

Si toutes les données sont sur un seul shard, suivez les étapes suivantes.

Vérifier que le balancer est activé :

```javascript
sh.getBalancerState()
```

Si la réponse est false, activez-le :

```javascript
sh.setBalancerState(true)
sh.getBalancerState()
```

Forcer le split des chunks :

```javascript
sh.splitAt("testDB.test", { _id: ObjectId("5f1a6b3b1c4ae35b2e0b8c6a") })
```

Remplacez `ObjectId("...")` par un `_id` existant dans votre base de données.

Tout d'abord, on compte le nombre total de documents dans la collection :

```javascript
db.test.count()
```

Si, par exemple, on obtient 25 357 documents, alors la moitié serait environ 12 678.

```javascript
db.test.find({}, { _id: 1 }).sort({ _id: 1 }).skip(12678).limit(1).pretty()
```

- `sort({ _id: 1 })` trie les documents par `_id` croissant.
- `skip(12678)` ignore les 12 678 premiers documents pour arriver vers le milieu.
- `limit(1)` récupère un seul document.
- `{ _id: 1 }` permet de n'afficher que le champ `_id`.

Déplacer un chunk vers un autre shard :

```javascript
sh.moveChunk("testDB.test", { _id: ObjectId("5f1a6b3b1c4ae35b2e0b8c6a") }, "sh1")
```

Encore une fois, remplacez l’_id par une valeur existante.

Vérifier la nouvelle répartition des chunks :

```javascript
db.test.getShardDistribution()
```