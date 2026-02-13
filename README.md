# Non-Relational Database Systems

A comprehensive study of NoSQL databases, distributed computing, and big data processing technologies including MongoDB, HBase, and Hadoop ecosystems.

## Table of Contents

- [Overview](#overview)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Components](#components)

## Overview

This repository contains practical implementations and exercises for learning non-relational database systems. It covers document stores (MongoDB), column-family databases (HBase), distributed processing (Hadoop MapReduce), and containerized deployment strategies.

## Technologies

- **MongoDB** - Document-oriented NoSQL database with replication and sharding
- **HBase** - Column-family database built on Hadoop
- **Hadoop MapReduce** - Distributed data processing framework
- **Docker** - Containerized database deployment

## Quick Start

### Prerequisites

- Docker Desktop
- Python 3.8+

### MongoDB Setup

```bash
# Start MongoDB containers
cd MongoDB/docker_setup
docker-compose up -d

# Initialize replica set
docker exec -it mongodb-primary mongosh
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongodb-primary:27017" },
    { _id: 1, host: "mongodb-secondary:27017" }
  ]
})

# Load sample data
docker exec -it mongodb-primary mongoimport \
  --db test --collection restaurants \
  --file /data/basic_operations/data/restaurants_dataset.json
```

### Hadoop MapReduce

```bash
# Test word count locally
cat Hadoop/data_samples/sample_input.txt | \
  python Hadoop/scripts/mappers/word_count_mapper.py | \
  sort | \
  python Hadoop/scripts/reducers/word_count_reducer.py
```

## Components

### Big Data Fundamentals
- **4 V's**: Volume, Variety, Velocity, Veracity
- **CAP Theorem**: Consistency, Availability, Partition tolerance
- **NoSQL Categories**: Key-Value, Document, Column-Family, Graph
- **Architecture Patterns**: Lambda vs Kappa architectures

### MongoDB Operations
- **Basic Operations**: CRUD, indexing, aggregation pipelines
- **Advanced Features**: Replica sets, sharding, geospatial queries
- **Sample Datasets**: Restaurant data (25K+ records), DBLP academic publications

### HBase Implementation
- **Master-Slave Architecture**: HMaster, RegionServers, ZooKeeper coordination
- **Column-Family Storage**: Efficient column-oriented data organization
- **Integration**: Hadoop ecosystem compatibility

### Hadoop MapReduce
- **Programming Model**: Map-Reduce paradigm for distributed processing
- **Implementations**: Word count, temperature analysis, log processing, averaging
- **Data Processing**: Weather data, log analysis, key-value operations

## Usage Examples

### MongoDB Queries

```javascript
// Find restaurants by cuisine with aggregation
db.restaurants.aggregate([
  { $match: { "grades.score": { $gt: 90 } } },
  { $group: {
    _id: "$cuisine",
    count: { $sum: 1 },
    avgScore: { $avg: "$grades.score" }
  }},
  { $sort: { avgScore: -1 } }
])
```

### MapReduce Processing

```bash
# Temperature analysis
hadoop jar hadoop-streaming.jar \
  -input /data/weather_data.txt \
  -output /output/max_temp \
  -mapper scripts/mappers/mapper_max_temp.py \
  -reducer scripts/reducers/reducer_max_temp.py
```
---

**Note**: This project is designed for educational purposes and demonstrates various NoSQL database concepts, distributed computing patterns, and practical implementations using modern containerization technologies.