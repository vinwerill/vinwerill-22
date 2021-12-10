# 高雄市公有路外停車場一覽表
import sys
import urllib.request
import json
import csv

def fetch(query_limit):
    # 指定查詢筆數上限
    url = 'http://data.kcg.gov.tw/api/action/datastore_search?resource_id=cd53c749-abeb-47db-b58c-5954d6c337a1'
    if query_limit > 0:
        url = url+'&limit={}'.format(query_limit)
    req = urllib.request.urlopen(url)

    # 確認資料庫編碼 (utf-8)
    charset = req.info().get_content_charset()
    # print('資料庫編碼:', charset)

    # response_data = req.read().decode(charset)
    response_data = req.read()
    # 全部資料
    json_data = json.loads(response_data)
    return json_data


if __name__ == '__main__':
    qlimit = int(input('設定查詢筆數 (0.all | -1.quit): '))
    if qlimit == -1:
        sys.exit()
    json_data = fetch(qlimit)
    print(json.dumps(json_data, sort_keys=True, indent=4), file=open('parking.json', 'wt'))

    print('停車場欄位:')
    for col in json_data['result']['fields']:
        print(col)

    print('\n'+'停車場資料:')
    for row in json_data['result']['records']:
        print(row)

    # encoding='utf8' (不支援 ASCII)
    # newline='' (若未設定，每列後會再斷行)
    parking_data = json_data['result']['records']
    with open('parking.csv', 'w', newline='', encoding='utf8') as parking_csv:
        # 資料寫入檔案
        csvwriter = csv.writer(parking_csv)
        count = 0
        for row in parking_data:
            if count == 0:
                header = row.keys()
                csvwriter.writerow(header)
            count += 1
            csvwriter.writerow(row.values())
    print('\n'+'資料筆數:', count)
