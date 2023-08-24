import os
import time
import json

import py_vncorenlp

from function import NeoAdapter


model = py_vncorenlp.VnCoreNLP(save_dir="/home/dungnguyen/work/model/vncorenlp")
neo = NeoAdapter(host="10.9.3.209", port="1918", password="password")

# convert raw text to json node and relationship data
with open("/home/dungnguyen/work/Neo4j-dependency-parsing/data/raw_text/doc_01.txt", "r") as f:
    doc = f.read()
docs = [doc]

nodes = {"data":[]}
relationships = {"data":[]}

for doc_id, doc in enumerate(docs):
    nlp_doc = model.annotate_text(doc)
    for sentence_id in nlp_doc.keys():
        nlp_sen = nlp_doc[sentence_id]
        for nlp_word in nlp_sen:
            word_data = {
                "wordForm": nlp_word["wordForm"],
                "posTag": nlp_word["posTag"] # label
            }
            nodes["data"].append(word_data)

            relationship_data = {
                "start_word": nlp_sen[nlp_word["head"]-1]["wordForm"] if nlp_word["head"] != 0 else nlp_word["wordForm"],
                "start_posTag": nlp_sen[nlp_word["head"]-1]["posTag"] if nlp_word["head"] != 0 else nlp_word["posTag"],
                "end_word": nlp_word["wordForm"],
                "end_posTag": nlp_word["posTag"],
                "depLabel": nlp_word["depLabel"], # label
                "doc_id": doc_id,
                "sentence_id": sentence_id
            }
            relationships["data"].append(relationship_data)


saved_dir = "/home/dungnguyen/work/Neo4j-dependency-parsing/docker-neo4j/import"

with open(os.path.join(saved_dir, 'Nodes.json'), 'w', encoding='utf8') as f:
    json.dump(nodes, f, ensure_ascii=False)

with open(os.path.join(saved_dir, 'Relationships.json'), 'w', encoding='utf8') as f:
    json.dump(relationships, f, ensure_ascii=False)

print("Finish converting raw text to json nodes and relationships data")


# clean database 
neo.clear_database()
init_time = time.time()

# import nodes
start_time = time.time()
query = """
    CALL apoc.periodic.iterate(
        'CALL apoc.load.json("file:///Nodes.json") YIELD value UNWIND value.data AS node RETURN node',
        'MERGE (:Word {wordForm:node.wordForm, posTag:node.posTag})',
        { batchSize:1000}
    )
"""
neo.run_query(query)

query = """
    MATCH (w:Word)
    CALL apoc.create.addLabels( w, [ toString(w.posTag) ] )
    YIELD node
    RETURN node;
"""
neo.run_query(query)
print(f"Fininised importing nodes: {time.time() - start_time}")


# import relationships
start_time = time.time()
query = """
    CALL apoc.periodic.iterate(
        'CALL apoc.load.json("file:///Relationships.json") YIELD value UNWIND value.data AS edge RETURN edge',
        'MATCH (head:Word {wordForm:edge.start_word, posTag:edge.start_posTag}), (tail:Word {wordForm:edge.end_word, posTag:edge.end_posTag}) MERGE (head)-[r:DP {depLabel:edge.depLabel}]->(tail)',
        {batchSize:100}
    )
"""
neo.run_query(query)


print(f"Fininised importing relationships: {time.time() - start_time}")

print(f"\nTotal runtime: {time.time() - init_time}")