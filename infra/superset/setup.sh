git clone https://github.com/apache/superset.git
cd superset
touch ./docker/requirements-local.txt
echo "clickhouse-connect" >> ./docker/requirements-local.txt
docker compose -f docker-compose-non-dev.yml up