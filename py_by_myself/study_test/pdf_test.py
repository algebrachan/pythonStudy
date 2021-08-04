import PyPDF2
pdfFileObj = open('1.pdf','rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
print(pdfReader.numPages)
pageObj = pdfReader.getPage(12)
a = pageObj.extractText()
print(a)