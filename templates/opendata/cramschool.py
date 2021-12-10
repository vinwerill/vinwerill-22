# 高雄市公有路外停車場一覽表
import sys
import urllib.request
import json
import csv

def fetch(query_limit):
    # 指定查詢筆數上限
    url = 'http://bsb.kh.edu.tw/afterschool/opendata/afterschool_json.jsp?city=70'
    req = urllib.request.urlopen(url)

    # 確認資料庫編碼 (utf-8)
    charset = req.info().get_content_charset()
    # print('資料庫編碼:', charset)

    # response_data = req.read().decode(charset)
    response_data = req.read()
    # 全部資料
    json_data = json.loads(response_data)
    if query_limit==0:
         return json_data[:len(json_data)+1]
    return json_data[:query_limit]


if __name__ == '__main__':
    qlimit = int(input('設定查詢筆數 (0.all | -1.quit): '))
    if qlimit == -1:
        sys.exit()
    json_data = fetch(qlimit)
    print(json.dumps(json_data, sort_keys=True, indent=4), file=open('cram_school.json', 'wt'))
    print('停車場欄位:')
    for col in json_data:
        print(col['短期補習班名稱']+':'+col['短期補習班類別'])


    # encoding='utf8' 
    # newline=''
    cram_school_data = json_data
    with open('cram_school.csv', 'w', newline='', encoding='utf8') as cram_school_csv:
        # 資料寫入檔案
        csvwriter = csv.writer(cram_school_csv)
        count = 0
        for row in cram_school_data:
            if count == 0:
                header = row.keys()
                csvwriter.writerow(header)
            count += 1
            csvwriter.writerow(row.values())
    print('\n'+'資料筆數:', count)
    