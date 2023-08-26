import os
import time
import re
import json

import py_vncorenlp

from .neo4j_adapter import NeoAdapter


NEO4J_IMPORT_DIR = "/home/dungnguyen/work/Neo4j-dependency-parsing/docker-neo4j/import"
neo = NeoAdapter(host="0.0.0.0", port="7687", password="12345678")
vncorenlp_model = py_vncorenlp.VnCoreNLP(
    save_dir="/home/dungnguyen/work/Neo4j-dependency-parsing/model/vncorenlp"
)


def convert_article_to_raw_text(article):
    title = article.title
    snippet = article.snippet
    message = article.message

    punct = [".", "!", "?", ",", ":", ";"]
    for text in [title, snippet, message]:
        if text and text[-1] not in punct:
            text += "."

    content = title + " " + snippet + " " + message
    content = re.sub(r"\s+", " ", content)
    content = content.strip()

    return content


def convert_articles_to_neo4j_imported_files(articles):
    start_time = time.time()
    nodes = {"data": []}
    relationships = {"data": []}

    for article in articles:
        content = convert_article_to_raw_text(article)

        nlp_doc = vncorenlp_model.annotate_text(content)
        for sentence_id in nlp_doc.keys():
            nlp_sen = nlp_doc[sentence_id]
            for nlp_word in nlp_sen:
                word_data = {
                    "wordForm": nlp_word["wordForm"],
                    "nerLabel": nlp_word["nerLabel"],
                    "posTag": nlp_word["posTag"],  # label
                }
                if word_data not in nodes["data"]:
                    nodes["data"].append(word_data)

                relationship_data = {
                    "start_word": nlp_sen[nlp_word["head"] - 1]["wordForm"]
                    if nlp_word["head"] != 0
                    else nlp_word["wordForm"],
                    "start_posTag": nlp_sen[nlp_word["head"] - 1]["posTag"]
                    if nlp_word["head"] != 0
                    else nlp_word["posTag"],
                    "end_word": nlp_word["wordForm"],
                    "end_posTag": nlp_word["posTag"],
                    "depLabel": nlp_word["depLabel"],  # label
                    # "doc_id": doc_id,
                    # "sentence_id": sentence_id
                }
                if relationship_data not in relationships["data"]:
                    relationships["data"].append(relationship_data)

    with open(os.path.join(NEO4J_IMPORT_DIR, "Nodes.json"), "w", encoding="utf8") as f:
        json.dump(nodes, f, ensure_ascii=False)

    with open(
        os.path.join(NEO4J_IMPORT_DIR, "Relationships.json"), "w", encoding="utf8"
    ) as f:
        json.dump(relationships, f, ensure_ascii=False)

    print(
        f"Fininised converting articles to Neo4j import files: {time.time() - start_time}"
    )


def import_data_to_neo4j_db():
    # clean database
    start_time = time.time()
    neo.clear_database()
    print(f"Fininised clearing old data: {time.time() - start_time}")

    # import nodes
    start_time = time.time()
    query = """
        CALL apoc.periodic.iterate(
            'CALL apoc.load.json("file:///Nodes.json") YIELD value UNWIND value.data AS node RETURN node',
            'MERGE (:Word {wordForm:node.wordForm, posTag:node.posTag, nerLabel:node.nerLabel})',
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


def import_articles(articles):
    init_time = time.time()
    try:
        convert_articles_to_neo4j_imported_files(articles)
    except:
        return {
            "is_success": False,
            "status": -1,
            "res": [],
            "msg": "cannot convert articles data to Neo4j imported files",
        }
    try:
        import_data_to_neo4j_db()
    except:
        return {
            "is_success": False,
            "status": -1,
            "res": [],
            "msg": "cannot import_data_to_neo4j_db",
        }

    print(f"\nTotal import time: {time.time() - init_time}")
    return {
        "is_success": True,
        "status": 2,
        "res": [],
        "msg": "import data successfully",
    }
