import py_vncorenlp

# py_vncorenlp.download_model(save_dir='/home/dungnguyen/work/model/vncorenlp')
model = py_vncorenlp.VnCoreNLP(save_dir='/home/dungnguyen/work/model/vncorenlp')


# # Annotate a raw corpus
model.annotate_file(input_file="/home/dungnguyen/work/Neo4j-dependency-parsing/data/raw_text/doc_00.txt", output_file="/home/dungnguyen/work/Neo4j-dependency-parsing/data/raw_text/doc_00_vnc.txt")

# Annotate a raw text
# model.print_out(model.annotate_text("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây."))

