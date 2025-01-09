from sentence_transformers import SentenceTransformer
class EmbeddingModel:
    def __init__(self,model_path):
        print("importing embedding ......")
        self.model = SentenceTransformer(model_path)
        print("import embedding model succeed")
    def embed(self,content_list):
        return self.model.encode(content_list)