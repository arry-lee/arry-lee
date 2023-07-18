from datetime import datetime
import json

def json2markdown(json_data):
    data = json_data['readBooks']
    # data = json.loads(json_data)

    # 构建 Markdown 表头
    headers = ["bookId", "title", "author", "cover","startReadingTime", "finishTime", "markStatus", "progress", "readtime",]

    # 构建 Markdown 表格内容
    rows = ["| " + " | ".join(headers) + " |"]
    rows.append("| " + " | ".join(['---' for i in headers]) + " |")
    count = 1
    for item in data:
        if item['bookId'][0].isalpha():
            continue
        item['bookId'] = count
        count += 1
        item['startReadingTime'] = datetime.fromtimestamp(item.get("startReadingTime")).strftime("%Y-%m-%d %H:%M:%S")
        if item.get("finishTime"):
            item['finishTime'] = datetime.fromtimestamp(item.get("finishTime")).strftime("%Y-%m-%d %H:%M:%S")
        else:
            item["finishTime"] = "-"

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

with open('../books/books0.json','r',encoding='utf-8') as f:
    data = json.load(f)
    table = json2markdown(data)

with open('../books/books0.md', 'w', encoding='utf-8') as f:
    f.write(table)
