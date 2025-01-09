## RAGKB
基于Flask构建

### Version
Now Version：2025-1-2-v1

| Version      | Description |
| -----------  | ----------- |
| 2025-1-1-v1  | 初步构建聊天机器人，实现基本问答界面与问答功能以及登录功能       |
| 2025-1-2-v1  | 丰富了登录界面，添加了上传文档功能，但并未与大模型关联        |
| 2025-1-9-v1| 开发了RAG功能，上传文档后自动分段编码为向量并存储，提问时对问题进行检索，讲检索的内容和问题一并提交给大模型 |


### Download
```shell
git clone https://github.com/idlzy/RAGKB.git
cd RAGKB
```

### Download Embedding Model
通过百度网盘分享的文件：paraphrase-multilingual-MiniLM-L12-...
链接：https://pan.baidu.com/s/16O6FlUdJXzNM8g5uvR_ffQ?pwd=sj5r 
提取码：sj5r 
--来自百度网盘超级会员V5的分享

将模型文件放入到工程根目录即可