#!/bin/bash
while [ "true" ]
do
    cd /home/dungnguyen/work/Neo4j-dependency-parsing
    source /home/dungnguyen/work/Neo4j-social-network/venv/bin/activate 
    python main_service.py
    sleep 5
done