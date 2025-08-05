# Guide for 3 MapReduce Exercises

**Note:** Make sure your Docker network (`hadoop`) is already created and that you have pulled the image `liliasfaxi/hadoop-cluster:latest`.

## 1. Start the Hadoop Cluster

### 1.1 Launch the Master and Worker Containers

```bash
# Start the Hadoop master node
docker run -itd --net=hadoop -p 50070:50070 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/hadoop-cluster:latest

# Start the first worker node
docker run -itd -p 8040:8042 --net=hadoop --name hadoop-worker1 --hostname hadoop-worker1 liliasfaxi/hadoop-cluster:latest

# Start the second worker node
docker run -itd -p 8041:8042 --net=hadoop --name hadoop-worker2 --hostname hadoop-worker2 liliasfaxi/hadoop-cluster:latest
```

### 1.2 Enter the Master and Start Hadoop

```bash
docker exec -it hadoop-master bash
./start-hadoop.sh
jps   # Verify that NameNode, ResourceManager, etc. are running
```

## 2. Upload Input Files and Copy Scripts to the Hadoop Master

You need to copy the input files and your mapper/reducer scripts for each exercise from your host into the master container.

### 2.1 Copy Input Files

From your host machine, run:

```bash
# Exercise 1 input file: donnees_cle_valeur_plus.txt
docker cp donnees_cle_valeur_plus.txt hadoop-master:/root/donnees_cle_valeur_plus.txt

# Exercise 2 input file: weather_data.txt
docker cp weather_data.txt hadoop-master:/root/weather_data.txt

# Exercise 3 input file: log_data.txt
docker cp log_data.txt hadoop-master:/root/log_data.txt
```

### 2.2 Copy Mapper and Reducer Scripts

For Exercise 1 (Average Value per Key):

```bash
docker cp mapper_avg.py hadoop-master:/root/mapper_avg.py
docker cp reducer_avg.py hadoop-master:/root/reducer_avg.py
```

For Exercise 2 (Maximum Temperature per City):

```bash
docker cp mapper_max_temp.py hadoop-master:/root/mapper_max_temp.py
docker cp reducer_max_temp.py hadoop-master:/root/reducer_max_temp.py
```

For Exercise 3 (Filter Logs by "ERROR" Level):

```bash
docker cp mapper_max_temp.py hadoop-master:/root/mapper_filter_error.py
docker cp reducer_max_temp.py hadoop-master:/root/reducer_filter_error.py
```

Then, for each input file, upload it to HDFS. For example:

```bash
# Exercise 1: Upload donnees_cle_valeur_plus.txt
hdfs dfs -put /root/donnees_cle_valeur_plus.txt /test

# Exercise 2: Upload weather_data.txt
hdfs dfs -put /root/weather_data.txt /test

# Exercise 3: Upload log_data.txt
hdfs dfs -put /root/log_data.txt /test
```

4. Run the Hadoop Streaming Jobs
4.1 Exercise 1: Calculate the Average Value per Key
Mapper Script: mapper_avg.py
Reducer Script: reducer_avg.py

Run the job with:

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /test/donnees_cle_valeur_plus.txt \
  -output /output/avg_results \
  -file /root/mapper_avg.py -mapper "python3 mapper_avg.py" \
  -file /root/reducer_avg.py -reducer "python3 reducer_avg.py"
```

Check Results:

```bash
hdfs dfs -ls /output/avg_results
hdfs dfs -cat /output/avg_results/part-00000
```

4.2 Exercise 2: Find the Maximum Temperature per City
Mapper Script: mapper_max_temp.py
Reducer Script: reducer_max_temp.py

Run the job with:

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /test/weather_data.txt \
  -output /output/max_temp_results \
  -file /root/mapper_max_temp.py -mapper "python3 mapper_max_temp.py" \
  -file /root/reducer_max_temp.py -reducer "python3 reducer_max_temp.py"
```
Check Results:


```bash
hdfs dfs -ls /output/max_temp_results
hdfs dfs -cat /output/max_temp_results/part-00000
```
4.3 Exercise 3: Filter Log Data by Severity Level ("ERROR")

Mapper Script: mapper_filter_error.py
Reducer Script: reducer_filter_error.py

Run the job with:

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /test/log_data.txt \
  -output /output/error_logs_results \
  -file /root/mapper_filter_error.py -mapper "python3 mapper_filter_error.py" \
  -file /root/reducer_filter_error.py -reducer "python3 reducer_filter_error.py"
```

Check Results:

```bash
hdfs dfs -ls /output/error_logs_results
hdfs dfs -cat /output/error_logs_results/part-00000
```