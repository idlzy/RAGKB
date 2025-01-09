from .fileparse import FileParser
from .embedding import EmbeddingModel
from .sql import load_vectors_from_mysql,get_metadata_from_mysql
import faiss

class VectorBase:
    def __init__(self,embedding_model,conn,CosineSimilarityThreshold=0.5):
        self.em = embedding_model
        self.fpr = FileParser()
        self.vectorbase = None
        self.vectorindex = None
        self.sqlindex = None
        self.CosineSimilarityThreshold = CosineSimilarityThreshold
        self.update(conn=conn)
    def generate(self,file_name,connection):
        content_list = self.fpr.ParseFile(file_name=file_name)
        vector = self.em.embed(content_list=content_list)
        cursor = connection.cursor()
        for v,c in zip(vector,content_list):
            sql = f"INSERT INTO kb (vectordata, metadata,source) VALUES (%s, %s, %s)"
            cursor.execute(sql, (v.tobytes(), c,file_name))
            connection.commit()
        print(f"文件{file_name}已解析至数据库")
        self.update(conn=connection)
    
    def update(self,conn):
        self.vectorbase,self.sqlindex = load_vectors_from_mysql(conn)
        # 构建 CPU 索引
        if self.vectorbase.ndim!=1:
            faiss.normalize_L2(self.vectorbase)
            self.vectorindex = faiss.IndexFlatIP(self.vectorbase.shape[1])  # 使用 L2 距离
            self.vectorindex.add(self.vectorbase)  # 添加向量到索引
            print("向量数据库已更新")
    
    def search(self,query,conn,k=5):
        query = [query]
        query_vector = self.em.embed(query)
        faiss.normalize_L2(query_vector)
        if self.vectorbase.ndim!=1:
            CosineSimilarities, indices = self.vectorindex.search(query_vector, k)
            res_list = []
            print(CosineSimilarities)
            for id_ ,cs in zip(indices[0],CosineSimilarities[0]):
                if cs < self.CosineSimilarityThreshold:
                    continue
                sql_id = self.sqlindex[id_]
                res = get_metadata_from_mysql(sql_id,conn)
                res_list.append(res)
            result = '\n'.join(res_list)
        else:
            result = ''
        return(result)