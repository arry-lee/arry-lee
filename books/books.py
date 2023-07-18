"""
要使用 mitmproxy 实现抓包，你可以按照以下步骤进行操作：

安装 mitmproxy：你可以使用 pip 或其他包管理工具来安装 mitmproxy。在命令行中运行以下命令：
pip install mitmproxy
启动 mitmproxy：在命令行中运行以下命令来启动 mitmproxy：
mitmproxy
这将启动 mitmproxy 并监听默认端口 8080。

配置手机代理：将手机的代理设置为运行 mitmproxy 的计算机的 IP 地址和端口号（默认为 8080）。你可以在手机的网络设置中找到代理设置，并将它配置为与 mitmproxy 监听的地址相对应。

打开应用程序并触发网络流量：在手机上打开你想要抓包的应用程序，并触发一些与网络通信相关的操作，例如发送请求或接收响应。

查看捕获的流量：在 mitmproxy 控制台上，你将能够看到捕获的网络流量。你可以使用键盘上的方向键来选择和浏览不同的请求和响应。通过按下回车键，你可以查看请求和响应的详细信息，包括 HTTP 头、内容等。

修改请求和响应（可选）：如果需要修改请求或响应，可以在 mitmproxy 控制台上编辑相应的字段。通过按下 e 键，你可以进入编辑模式，并修改需要更改的字段。按下回车键确认修改后，mitmproxy 将使用修改后的信息继续处理。

除了上述的命令行方式外，你还可以使用 mitmweb 进行图形化界面操作。只需在命令行中运行以下命令即可：

mitmweb
这将启动 mitmweb 服务器并监听默认端口 8081。然后，你可以通过在浏览器中访问 http://localhost:8081 来访问 mitmweb 的界面，进行类似的流量捕获和修改操作。

希望这些步骤能帮助你使用 mitmproxy 实现抓包。如果还有其他问题，请随时提问。




2023/7/17 13:53:38

mitmproxy 指定别的端口

2023/7/17 13:53:50

如果你想将 mitmproxy 监听在除了默认的端口 8080 之外的其他端口，你可以通过以下方式指定端口：

在命令行中运行以下命令来启动 mitmproxy，并指定所需的端口号：

mitmproxy -p <端口号>
例如，要将 mitmproxy 监听在端口号 8888 上，你可以运行以下命令：

mitmproxy -p 8888
此时，mitmproxy 将在指定的端口上进行监听，并捕获通过该端口的网络流量。

请记住，当你将 mitmproxy 更改为不同的端口时，你还需要相应地配置手机或应用程序的代理设置，以使其与 mitmproxy 监听的端口对应。

希望这能回答你的问题。如果还有其他疑问，请告诉我。
"""
import json
from datetime import datetime

import requests
from mitmproxy import http, ctx

requests.packages.urllib3.disable_warnings()


def request(flow: http.HTTPFlow) -> None:
    # 获取请求头信息
    headers = flow.request.headers
    if 'accessToken' in headers:
        with open('token', 'w') as f:
            f.write(headers['accessToken'])

        finish = 0
        data = get_readbook(headers, finish)

        with open(f'books{finish}.json', 'w', encoding='utf-8') as js:
            json.dump(data, js, ensure_ascii=False)

        table = json2markdown(data)
        with open(f'books{finish}.md', 'w', encoding='utf-8') as f:
            f.write(table)

        ctx.master.shutdown()


def get_readbook(headers):
    url = "https://i.weread.qq.com/mine/readbook"

    params = dict(vid=headers['vid'], star=0, yearRange="0_0", count=200, rating=0, listType=1)
    r = requests.get(url, params=params, headers=headers, verify=False)
    if r.ok:
        data = r.json()
    else:
        raise Exception(r.text)
    return data


def json2markdown(json_data):
    data = json_data['readBooks']
    headers = ["bookId", "title", "author", "cover", "startReadingTime", "finishTime", "markStatus", "progress",
               "readtime", ]

    # 构建 Markdown 表格内容
    rows = ["| " + " | ".join(headers) + " |", "| " + " | ".join(['---' for i in headers]) + " |"]
    count = 1
    for item in data:
        if item['bookId'][0].isalpha():
            continue
        item['bookId'] = count
        count += 1
        item['startReadingTime'] = datetime.fromtimestamp(item.get("startReadingTime")).strftime("%Y-%m-%d %H:%M:%S")
        item['finishTime'] = datetime.fromtimestamp(item.get("finishTime")).strftime("%Y-%m-%d %H:%M:%S")
        item['readtime'] = item.get("readtime") // 60  # 转换为分钟
        item['cover'] = f"![Cover]({item.get('cover', '')})"
        # 构建 Markdown 表格行
        row = [
            str(item.get(key, ""))
            for key in headers
        ]
        rows.append("| " + " | ".join(row) + " |")

    # 将表头和表格内容连接起来
    table = "\n".join(rows)

    return table


addons = [
    (".*", None),  # 匹配所有 URL
]

# if __name__ == '__main__':
#     os.system("mitmproxy -p 8888 -s books.py")
