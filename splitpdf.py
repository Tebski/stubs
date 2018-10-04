from PyPDF2 import PdfFileWriter, PdfFileReader
import os

dir_to_scan = os.path.join(os.path.curdir,"stubs")
files = os.listdir(dir_to_scan)

for f in files:
    bdateindex = f.find("ACHStubs_")
    edateindex = f.find(".pdf")
    idate = f[bdateindex+9:edateindex]
    print(idate)

ifile = "ACHStubs_9.5.2018.pdf"

inputpdf = PdfFileReader(open(os.path.join(dir_to_scan,ifile),"rb"))

for i in range(inputpdf.numPages):
    ofile = PdfFileWriter()
    ipage = inputpdf.getPage(i)
    itext = ipage.extractText()
    venindex = itext.find("Ven: ")
    vendor = itext[venindex+5:venindex+11].strip()

    print(vendor)

    ofile.addPage(ipage)
    with open(vendor + "_ACHStubs_9.5.2018.pdf","wb") as outputstream:
        ofile.write(outputstream)
