## Build and Start the Container 
1. Build the container with:
```
docker build -t influxdb3-app .
```
2. Start the container with: 
```
docker run -it \
  -v ./app/data:/app/data \
  -v ./app/plugins:/app/plugins \
  -v ./app/sample_write.py:/app/sample_write.py \
  -v ./app/telegraf.conf:/app/telegraf.conf \
  -p 8181:8181 \
  --user root \
  influxdb3-app serve \
  --node-id my_host \
  --object-store file \
  --data-dir /app/data \
  --plugin-dir /app/plugins
```
3. Start a new dev container in VS Code: 
```
> Dev Containers:Attach to a Running Container 
Terminal > New Terminal 
```
4. Change directories into /app:
```
cd /app
```

## Create resources 

5. Create a token 
```
influxdb3 create token
```
SAVE TOKEN HERE: 
apiv3_9RMgaDnWu-LxKBk98Q6IHiNan549VCsHu7GmP37nRjRC8uXSAjcfxZ8P5kqQQWWEsllP25xXMrhfVFu-6dWLrg

**Optional** Stop the influxdb3 server and start it again with the Hashed Token: 
```
grep -l "influxdb" /proc/*/cmdline | awk -F'/' '{print $3}'

kill -9 <PID>

influxdb3 serve \
--bearer-token <bearer token>
--node-id my_host \
--object-store file \
--data-dir /app/data \
--plugin-dir /app/plugins

```

6. Export token: 
```
export INFLUX_TOKEN=apiv3_qFilzqGc5cSwih505V3KRbe0BZEQkzsjr7YmsSffNj5LQOpvyceDjv4sZnc5NvxWM1nPzyXQZQF18oOybzwUrw
```

## Write and Query Data with Telegraf and the Python Client Library 
7. Run the sample_write.py 
```
python sample_write.py 
```

8. Query the database we just wrote to: 
```
influxdb3 query --database test -l sql 'SELECT * FROM "environmental_data"'
```

9. Start the telegraf config:
```
telegraf --config telegraf.conf
```

10.  Query the cpu database:
```
influxdb3 query --database cpu -l sql
 'SELECT * FROM "cpu"'
```

11.  List databases: 
```
influxdb3 show databases
```

## Create a Plugin and Enable a Python Processing Engine Trigger 
12. Install necessary packages: 
```
influxdb3 install package datetime
```

13. Test the plugin with:
```
influxdb3 test wal_plugin \
-d my_database \
--lp="sensor_data,location=living\\ room temperature=22.5 123456789" \
/app/plugins/example_processor.py
```

**Note** use `chmod 755 /app/plugins/` if you run into permission issues. 

14. Create a database with:
```
influxdb3 create database my_database
```

15.   Create a trigger with:
```
influxdb3 create trigger \
-d my_database \
--plugin-filename="/app/plugins/example_processor.py" \
--trigger-spec="all_tables"  \
standardize_iot
```

16.  Enable the plugin with:
```
influxdb3 enable trigger \
--database my_database  \
standardize_iot
```

17.  Test the plugin by writing data: 
```
influxdb3 write \
--database my_database \
"sensor_data,sensor=TempSensor1,location=living\\ room temperature=22.5"
```

18.  Query back to confirm: 
```
influxdb3 query \
--database unified_sensor_data \
"SELECT * FROM sensor_data"
```

## Create a Last Value Cache and Query it
18. C