# 高雄市公有路外停車場一覽表
import sys
import urllib.request
import json
import csv

def fetch(query_limit):
    # 指定查詢筆數上限
    url = 'https://ws.kinmen.gov.tw/001/Upload/0/relfile/0/0/92b4584c-f454-4bd5-a75f-818dcf901f32.json'
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
    print(json.dumps(json_data, sort_keys=True, indent=4), file=open('kinmen_tourist_spot.json', 'wt'))
    print('Quantity:')
    for col in json_data:
        print(col['CName']+':'+col['CAdd'])


    # encoding='utf8' 
    # newline=''
    kinmen_tourist_spot_data = json_data
    with open('kinmen_tourist_spot.csv', 'w', newline='', encoding='utf8') as kinmen_tourist_spot_csv:
        # 資料寫入檔案
        csvwriter = csv.writer(kinmen_tourist_spot_csv)
        count = 0
        for row in kinmen_tourist_spot_data:
            if count == 0:
                header = row.keys()
                csvwriter.writerow(header)
            count += 1
            csvwriter.writerow(row.values())
    print('\n'+'資料筆數:', count)
    