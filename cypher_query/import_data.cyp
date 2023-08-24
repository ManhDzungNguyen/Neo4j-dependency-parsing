CALL apoc.periodic.iterate(
    'CALL apoc.load.json("file:///Nodes.json") YIELD value UNWIND value.data AS node RETURN node',
    'MERGE ({wordForm:node.wordForm, posTag:node.posTag})',
    { batchSize:1000, iterateList: true , parallel: true }
)

CALL apoc.periodic.iterate(
    'CALL apoc.load.json("file:///Relationships.json") YIELD value UNWIND value.data AS edge RETURN edge',
    'MATCH (head {wordForm:edge.start_word, posTag:edge.start_posTag}), (tail {wordForm:edge.end_word, posTag:edge.end_posTag}) MERGE (head)-[{depLabel:edge.depLabel}]->(tail)',
    {batchSize:100}
)