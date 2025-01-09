import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



def get_file_type(file_name):
    file_extension = Path(file_name).suffix
    return file_extension

def ParsePDF(file_name,text_splitter):
    loader = PyPDFLoader(file_name)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 0,
    )
    docs = text_splitter.split_documents(pages)
    docs_txt = [doc.page_content for doc in docs]
    return docs_txt

def ParseDocx(file_name,text_splitter):
    loader = Docx2txtLoader(file_name)
    pages = loader.load_and_split()
    
    docs = text_splitter.split_documents(pages)
    docs_txt = [doc.page_content for doc in docs]
    return docs_txt

class FileParser:
    def __init__(self):
        self.docs_txt = None
        self.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 0,
    )
        
    def ParseFile(self,file_name):
        file_type = get_file_type(file_name)
        if file_type.lower() == '.docx':
            self.docs_txt = ParseDocx(file_name,self.text_splitter)
        elif file_type.lower() == '.pdf':
            self.docs_txt = ParsePDF(file_name,self.text_splitter)
        else:
            print("无法解析，请上传pdf或docx文件")
        return self.docs_txt