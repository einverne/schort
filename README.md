# schort - It's just a tiny link shortener

使用 Flask 和 sqlite 实现的短域名服务

原始仓库地址: <https://github.com/sqozz/schort>

## 安装使用

1. Clone this repo into e.g. /opt/schort
2. Create a user and adjust permissions to write at least into /opt/schort/data
2. Install requirements (see below)
3. Configure your wsgi or fcgi server
4. Configure your webserver that he talks to your wsgi/fcgi server


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
