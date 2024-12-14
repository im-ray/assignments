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





