#### 1. upload_csv endpoint
The upload_csv API allows users to easily upload datasets stored in CSV files by providing a direct link to a publicly accessible CSV file. This API automates the process of importing data, parsing it, and storing it in a database, saving time and reducing manual effort for data analysts.


Q1 : why clickhouse (column based ) not postgres(row based) ?
https://posthog.com/blog/clickhouse-vs-postgres


setup clickhouse in docker
https://www.propeldata.com/blog/clickhouse-docker

https://medium.com/@jayprakash.bilgaye/getting-started-with-clickhouse-on-docker-quick-and-easy-guide-for-mac-users-e69dcc138c6e

```
    docker pull clickhouse/clickhouse-server
```

```
    docker run -d --name segwise_clickhouse -p 8123:8123 -p 9000:9000 -e CLICKHOUSE_USER=rupesh -e CLICKHOUSE_PASSWORD=Rupesh123 -e CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1 clickhouse/clickhouse-server:latest
```



# Segwise AI - Backend Assignment

## Overview

This project is a backend application built using **Flask** and **ClickHouse**. The purpose of this application is to handle CSV file uploads, process them, and store the data into **ClickHouse**.

### Database Setup:
1. **ClickHouse** Database and Table are set up and initialized successfully when the app starts.
2. The **ClickHouse schema** is created with the following structure:

   ```sql
   CREATE DATABASE IF NOT EXISTS analytics;

   CREATE TABLE IF NOT EXISTS analytics.game_data (
       app_id Int64,
       name String,
       release_date DateTime,
       required_age Int64,
       price Float64,
       dlc_count Int64,
       about_the_game String,
       supported_languages String,
       windows UInt8,
       mac UInt8,
       linux UInt8,
       positive Int64,
       negative Int64,
       score_rank Float64,
       developers String,
       publishers String,
       categories String,
       genres String,
       tags String
   ) ENGINE = MergeTree()
   ORDER BY release_date;

### Testing with local csv file once the server is up and running
***(Make sure database is up and running before this setup, here i am running in docker)***
command to run the application and test with local csv file from the project directory

```
python run.py
```

```
curl -X POST -F "file=@game_data.csv" http://127.0.0.1:5000/upload_csv
```

```
curl -X POST -H "Content-Type: application/json" -d '{"csv_url": "https://example.com/your_csv_file.csv"}' http://127.0.0.1:5000/upload_csv_url
```


