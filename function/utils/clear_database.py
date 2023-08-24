import sys

sys.path.append("/home/dungnguyen/work/Neo4j-social-network")

import time

from function import NeoAdapter


neo = NeoAdapter(host="10.9.3.209", port="1918", password="password")

init_time = time.time()
res = neo.clear_database()
print(f"runtime: {time.time() - init_time}")
