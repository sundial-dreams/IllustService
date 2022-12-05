## Illustration 服务端
### 一、项目结构
```bash
|-data
|-logs
|-mock
|-model
|-resource
  |-large
  |-medium
  |-original
  |-square_medium
|-scripts
|-service
|-tools
```

### 二、Pixiv插画爬取与下载
`script`目录下的`download_from_users.py`为下载脚本，但需要先运行`get_users.py`获取画师id，下载后的插画位于resource下

需要开启mongodb存储结果
```bash
sudo mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --logappend
```
### 三、服务运行
```bash
python main.py
```