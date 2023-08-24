docker run \
    --name neo4j_dp \
    -p3592:7474 -p1918:7687 \
    -d \
    -v /home/dungnguyen/work/Neo4j-dependency-parsing/docker-neo4j/data:/data \
    -v /home/dungnguyen/work/Neo4j-dependency-parsing/docker-neo4j/logs:/logs \
    -v /home/dungnguyen/work/Neo4j-dependency-parsing/docker-neo4j/import:/var/lib/neo4j/import \
    -v /home/dungnguyen/work/Neo4j-dependency-parsing/docker-neo4j/plugins:/plugins \
    -e NEO4J_AUTH=neo4j/password \
    --env NEO4J_PLUGINS='["graph-data-science", "apoc"]' \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_AUTH=none \
    neo4j:5.10.0

chmod -R 777 /home/dungnguyen/work/Neo4j-dependency-parsing/docker-neo4j/import