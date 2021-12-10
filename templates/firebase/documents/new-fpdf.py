import urllib.request
import json
from fpdf import FPDF

word_levels = {'w1':'初級', 'w2':'中級', 'w3':'中高級'}
column_names = ['級別', '單字', '意義']
url = 'http://localhost:5000/gept/gept-words_json/{}'

for wl in word_levels.keys():
    req = urllib.request.urlopen(url.format(wl))
    response_data = req.read()
    json_data = json.loads(response_data)

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('msjh', '', 'C:\\Windows\\Fonts\\msjh.ttf', uni=True)

    # 檔案標題
    pdf.set_font('msjh', '', 16)
    pdf.set_text_color(0, 0, 255)
    pdf.write(8, '全民英檢{}字彙\n\n'.format(word_levels[wl]))

    # 字彙列表
    pdf.set_text_color(20, 20, 20)
    pdf.set_font('msjh', '', 11)
    total = 0
    counter = 0

    for letter in json_data['jsonData']:
        # 每個級別新增 100 字彙
        if total == 100:
            break
        # 每個字母新增 10 個字彙
        counter = 0
        for word in letter['words']:
            if counter != 0 and counter % 10 == 0:
                break
            # 新增單字的長度大於等於 5     
            if len(word[1]) >= 5:
                total += 1
                counter += 1
                word[0] = str(total)
                print(word)
                pdf.cell(10, 8, word[0], 1, 0, 'R')
                pdf.cell(30, 8, word[1], 1, 0, 'L')
                pdf.cell(150, 8, word[2], 1, 1, 'L')

    pdf.output('gept-words-{}.pdf'.format(wl), 'F')
