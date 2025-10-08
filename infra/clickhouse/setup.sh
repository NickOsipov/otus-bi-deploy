sudo service clickhouse-server start
sudo service clickhouse-server status

clickhouse-client # or "clickhouse-client --password" if you've set up a password.

# Check Query: SELECT now();

sudo vim /etc/clickhouse-server/config.d/available_connections.xml

# Add the following lines to the file:
<clickhouse>
<listen_host>0.0.0.0</listen_host>
</clickhouse>

sudo service clickhouse-server restart