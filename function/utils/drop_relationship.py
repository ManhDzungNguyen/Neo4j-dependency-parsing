import sys

sys.path.append("/home/dungnguyen/work/Neo4j-social-network")

import time

from function import NeoAdapter


neo = NeoAdapter(host="10.9.3.209", port="7687", password="12345678")

init_time = time.time()
res = neo.drop_relationship("COMMENTED_COMMON_POSTS")
print(res)
print(f"runtime: {time.time() - init_time}")
