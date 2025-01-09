import numpy as np
# 从 MySQL 中加载向量数据
def load_vectors_from_mysql(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, vectordata FROM kb;")
    results = cursor.fetchall()
    vectors = []
    ids = []
    for row in results:
        ids.append(row[0])  # 获取 ID
        vector = np.frombuffer(row[1], dtype=np.float32)  # 反序列化向量
        vectors.append(vector)
    cursor.close()
    return np.array(vectors), np.array(ids)

# 从 MySQL 中获取元数据
def get_metadata_from_mysql(ids,conn):
    cursor = conn.cursor()
    sql = "SELECT metadata FROM kb WHERE id = %s"
    cursor.execute(sql, (ids))
    result = cursor.fetchone()[0]
    cursor.close()
    return result
