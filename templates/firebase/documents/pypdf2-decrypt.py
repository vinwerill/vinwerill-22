import os
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter

wordLevels = ('w1', 'w2', 'w3')
password = 'swordfish'

for wl in wordLevels:
    filename = 'gept-words-{}-encrypted.pdf'.format(wl)
    pdfFile = open(filename, 'rb')
    pdfReader = PdfFileReader(pdfFile)
    if pdfReader.isEncrypted:
        pdfReader.decrypt(password)
        pdfWriter = PdfFileWriter()

        for pageNum in range(pdfReader.numPages):
            pdfWriter.addPage(pdfReader.getPage(pageNum))

        resultPdf = open('gept-words-{}-decrypted.pdf'.format(wl), 'wb')
        pdfWriter.write(resultPdf)
        resultPdf.close()
        print(filename+' has been decrypted.')
        
    else:
        print(filename+' is not encrypted.')
