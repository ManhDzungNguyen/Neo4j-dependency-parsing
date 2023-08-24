MATCH graph=(n1:N|Np|Ny { wordForm: "Bắc_Cực" })-[]-(action:V
WHERE action.wordForm <> "là")-[r1
WHERE r1.depLabel="sub"]->(n2:N|Np|Ny)-[r
WHERE r.depLabel="nmod"]-()
RETURN graph
