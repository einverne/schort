# schort - It's just a tiny link shortener

使用 Flask 和 sqlite 实现的短域名服务

原始仓库地址: <https://github.com/sqozz/schort>

## 安装使用

### 源码

    pip install -r requirements.txt
    flask db upgrade
    ./run.sh

### Docker

    sudo docker built -t schort .
    sudo docker run --name schort -p 4000:4000 schort

## 原理
取了原始链接的url safe BASE64

## Requirements:

见 requirements.txt

## Example

提交请求

```
curl -X POST --data 'url=https://google.com' localhost:4000
{
  "code": "success",
  "data": "",
  "msg": "http://localhost:4000/BQRv"
}
```

获取

```
curl -I "http://localhost:4000/BQRv"
HTTP/1.0 301 MOVED PERMANENTLY
Content-Type: text/html; charset=utf-8
Content-Length: 243
Location: https://google.com
Server: Werkzeug/0.14.1 Python/3.6.1
Date: Mon, 14 May 2018 03:30:38 GMT
```
