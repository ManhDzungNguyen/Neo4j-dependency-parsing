MATCH graph = (n1:N|Np|Ny { wordForm: "Bắc_Cực" })-[]-(a:V WHERE a.wordForm <> "là")-[r1 WHERE r1.depLabel="sub"]->(n2:N|Np|Ny)-[r WHERE r.depLabel="nmod"]-()
RETURN graph


MATCH graph = (n1:N|Np|Ny WHERE n1.wordForm IN ["Dương_Tuấn_Ngọc", "Ngọc"])<-[r1 WHERE r1.depLabel="sub"]-(action:V)-[r2]-(n2:N|Np|Ny)-[r]-()
RETURN graph


MATCH graph = 
(n1:N|Np WHERE n1.wordForm IN ["Dương_Tuấn_Ngọc", "Ngọc"])
<-[r1 WHERE r1.depLabel="sub"]-(action:V)-[r2 WHERE r2.depLabel IN ["dob"]]-(n2:N|Np|Ny)-[r3 WHERE r3.depLabel IN ["nmod"]]-(a0:A)
RETURN graph

// Xác định ra các hành động chính của 1 đối tượng
MATCH g=(n1 WHERE n1.nerLabel IN ["B-PER"])-[r1 WHERE r1.depLabel="sub"]-(v:V)-[r2 WHERE r2.depLabel="dob"]-()
RETURN g