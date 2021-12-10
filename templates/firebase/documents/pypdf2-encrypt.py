import PyPDF2

wordLevels = ('w1', 'w2', 'w3')
password = 'swordfish'

for wl in wordLevels:
    pdfFile = open('gept-words-{}.pdf'.format(wl), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    pdfWriter = PyPDF2.PdfFileWriter()

    for pageNum in range(pdfReader.numPages):
        pdfWriter.addPage(pdfReader.getPage(pageNum))
        
    pdfWriter.encrypt(password)
    resultPdf = open('gept-words-{}-encrypted.pdf'.format(wl), 'wb')
    pdfWriter.write(resultPdf)
    resultPdf.close()