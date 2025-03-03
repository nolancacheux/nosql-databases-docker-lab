# Practical Work: Running a Hadoop MapReduce Job in a Docker-Based Cluster

## Objective
The goal of this practical session is to deploy a Hadoop cluster using Docker, process a text file with MapReduce, and analyze the results. The job will count word occurrences from an input text file (`input.txt`).

## Step 1: Set Up the Hadoop Cluster in Docker
We need to create a Hadoop cluster inside Docker with one master node and two worker nodes.

### 1.1 Start the Hadoop Master Node
Run the following command to launch the Hadoop master node:

```bash
docker run -itd --net=hadoop -p 50070:50070 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/hadoop-cluster:latest
```

**Options Explained:**

- `--net=hadoop`: Assigns the container to the Hadoop network.
- `-p 50070:50070`, etc.: Maps ports for accessing Hadoop services.
- `--name hadoop-master`: Names the container `hadoop-master`.
- `--hostname hadoop-master`: Sets the hostname inside the container.
- `liliasfaxi/hadoop-cluster:latest`: Uses an existing Hadoop image.

### 1.2 Start the Worker Nodes
We need two workers to form a distributed system.

**Start Worker 1**

```bash
docker run -itd -p 8040:8042 --net=hadoop --name hadoop-worker1 --hostname hadoop-worker1 liliasfaxi/hadoop-cluster:latest
```

**Start Worker 2**

```bash
docker run -itd -p 8041:8042 --net=hadoop --name hadoop-worker2 --hostname hadoop-worker2 liliasfaxi/hadoop-cluster:latest
```

## Step 2: Start Hadoop Services
To start the Hadoop cluster, we need to access the `hadoop-master` container and run the initialization script.

### 2.1 Enter the Hadoop Master Node

```bash
docker exec -it hadoop-master bash
```

### 2.2 Start Hadoop

```bash
./start-hadoop.sh
```

This command will:

- Start the Namenode.
- Start YARN ResourceManager and NodeManagers.
- Launch HDFS (Hadoop Distributed File System).

### 2.3 Verify Running Hadoop Processes
To confirm that Hadoop services are running correctly, execute:

```bash
jps
```

Expected output should list:

- NameNode
- ResourceManager
- SecondaryNameNode
- Jps (Java Process Status)

## Step 3: Upload Input Data to HDFS

### 3.1 Remove Old Data from HDFS (if needed)
If a previous input file exists, remove it to avoid conflicts:

```bash
hdfs dfs -rm -r /test
hdfs dfs -rm -r /output
```

### 3.2 Copy the New Input File from Local System to Docker
Run this from your host machine to copy `input.txt` to `hadoop-master`:

```bash
docker cp input.txt hadoop-master:/root/input.txt
```

### 3.3 Create an HDFS Directory for the Input File
Inside the `hadoop-master` container:

```bash
hdfs dfs -mkdir /test
```

### 3.4 Upload the Input File to HDFS

```bash
hdfs dfs -put /root/input.txt /test
```

### 3.5 Verify the File is in HDFS

```bash
hdfs dfs -ls /test
```

Expected output:

```css
-rw-r--r--   1 root supergroup   [size]  [date]  /test/input.txt
```

 
## Step 3.3: Copy Mapper and Reducer Scripts to Hadoop Master

From your host machine, copy the `mapp.py` and `reducer.py` scripts to the `hadoop-master` container:

```bash
docker cp mapp.py hadoop-master:/root/mapp.py
docker cp reducer.py hadoop-master:/root/reducer.py
```
## Step 4: Test the Mapper and Reducer Scripts
Before running the MapReduce job, test the Python scripts manually.

### 4.1 Test the Mapper

```bash
cat /root/input.txt | python3 /root/mapp.py
```

Expected output:

```python-repl
word1   1
word2   1
word3   1
...
```

### 4.2 Test the Reducer

```bash
cat /root/input.txt | python3 /root/mapp.py | python3 /root/reducer.py
```

Expected output:

```python-repl
word1   3
word2   5
word3   2
...
```

If the output is empty or incorrect, debug the scripts before proceeding.

## Step 5: Execute the Hadoop Streaming Job

### 5.1 Run the MapReduce Job

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -input /test/input.txt \
    -output /output/results \
    -file /root/mapp.py -mapper "python3 mapp.py" \
    -file /root/reducer.py -reducer "python3 reducer.py"
```

**What happens here?**

- The mapper reads the input file and outputs (word, 1).
- Hadoop sorts and shuffles the words.
- The reducer sums up occurrences of each word.
- The final result is stored in HDFS.

## Step 6: Check the Results

### 6.1 List the Output Directory

```bash
hdfs dfs -ls /output/results
```

Expected output:

```pgsql
Found 2 items
-rw-r--r--   2 root supergroup          0 2025-02-24 10:33 /output/results/_SUCCESS
-rw-r--r--   2 root supergroup         [size] 2025-02-24 10:33 /output/results/part-00000
```

`_SUCCESS` confirms the job completed successfully.

### 6.2 View the Output

```bash
hdfs dfs -cat /output/results/part-00000
```

Expected output:

```css
code    1
hello   3
i       1
love    1
world   2
```

If the output is empty, verify that the `mapp.py` and `reducer.py` scripts are working correctly.

## Step 7: Re-run the Job with a New Input File
If you need to run the job again with a new input file, follow these steps:

**Delete the old data:**

```bash
hdfs dfs -rm -r /test
hdfs dfs -rm -r /output
```

**Copy the new `input.txt`:**

```bash
docker cp input.txt hadoop-master:/root/input.txt
```

**Re-upload to HDFS:**

```bash
hdfs dfs -mkdir /test
hdfs dfs -put /root/input.txt /test
```

**Run the MapReduce job again:**

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -input /test/input.txt \
    -output /output/results \
    -file /root/mapp.py -mapper "python3 mapp.py" \
    -file /root/reducer.py -reducer "python3 reducer.py"
```

**Check results:**

```bash
hdfs dfs -cat /output/results/part-00000
```

## Conclusion
This step-by-step guide documented every stage of running a MapReduce job in a Docker-based Hadoop cluster. You successfully:

- Set up Hadoop in Docker.
- Uploaded data to HDFS.
- Executed MapReduce scripts.
- Verified results.