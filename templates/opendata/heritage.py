# 高雄市文化資產
import urllib.request
import json
from random import sample

def fetch(query_limit):
    url = 'http://opendata.khcc.gov.tw/public/OD_Heritage.ashx'
    retries = 1
    while True:
        try:
            with urllib.request.urlopen(url, timeout=5) as req:
                response_data = req.read()
                break
        except:
            print('Timeout:', retries)
            retries += 1
    json_data = json.loads(response_data)
    if query_limit > 0:
        return sample(json_data, query_limit)
    return json_data


if __name__ == '__main__':
    json_data = fetch(0)
    print(json.dumps(json_data, sort_keys=True, indent=4), file=open('heritage.json', 'wt'))

    count = 0
    for row in json_data:
        # 印出欄位
        if count == 0:
            header = row.keys()
            print(header)
        # 印出資料
        print('\n' + '-'*80 + '\n')
        for key, value in row.items():
            print(key, ':', value)
        count += 1
    print('\n', '資料筆數:', count)
