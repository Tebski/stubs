'''
Script to process .txt files from glovia, and convert to PDF

Version 1.2
Added ability to split txt file based on vendor, as page breaks from the text
file appear unreliable
Suppress first line as it contains a page number which could be confusing to the end user
Modified script to run from the /stubs/ folder.

Version 1.1
Separated files into subfolders to make directory cleaner.
Removed last page if its blank to prevent empty pdfs being created

Version 1.0
Initial concept. Split txt files from Glovia based on page breaks. One page per vendor.
Produce a PDF for each page named after the vendor and the orginal
date/time stamp of the text fileself.
Naming conventions:
Input file is of type .txt and named ACHStubs_<date/time stamp>.txt
Output file is of type .pdf and named <vendor>_<date/time stamp.pdf
Script can process multiple input files, and will work so long as date/time stamp is
unique for each to prevent conflicts with same vendor being in each.

Vendor must appear in the page of the text file.
'''


import os
from fpdf import FPDF

ATTACH_SUB_DIR = 'attachments'
ARCHIVE_SUB_DIR = 'archive'
TXT_SUB_DIR = 'text'
HOME_DIR = os.path.curdir
DIR_TO_SCAN = os.path.join(HOME_DIR, TXT_SUB_DIR)
DIR_ARCHIVE = os.path.join(HOME_DIR, ARCHIVE_SUB_DIR)
DIR_ATTACH = os.path.join(HOME_DIR, ATTACH_SUB_DIR)
files = os.listdir(DIR_TO_SCAN)
valid_file = True




# Process files
for f in files:
    print("processing: " + f)
    bdateindex = f.find("ACHStubs_")
    edateindex = f.find(".txt")

    if edateindex == -1 or bdateindex == -1:
        valid_file = False
    else:
        valid_file = True

    if valid_file:
        idate = f[bdateindex+9:edateindex]
        print(idate)
        with open(os.path.join(DIR_TO_SCAN, f), "r") as ifile:
            txt = ifile.read()
            #check if it contains multiple pages
            if txt.count('MDC  C_ACHSTB') > 1:
                #multiple headers found
                if txt.count('\f') == 0:
                    #no page breaks found, need to insert them
                    start = 10 #ignore first occurence
                    pos = 1
                    while pos < len(txt) and pos > 0:
                        pos = txt.find('MDC  C_ACHSTB', start)
                        if pos > -1:
                            txt = txt[:pos-1] + '\f' + txt[pos:]
                            start = pos+1

            #split on page break
            pages = txt.split("\f")
            #remove last page (if it's blank)
            if len(pages[-1].strip()) == 0:
                print("Empty page")
                pages.pop()

            for page in pages:
                venindex = page.find("Ven: ")
                if venindex == -1:
                    print("no vendor found in " + f)
                else:
                    vendor = page[venindex+5:venindex+11].strip()
                    print("Processing vendor: " + vendor)
                    page = page[page.find('\n')+1:] #suppress first line
                    pdf = FPDF(format="letter")
                    pdf.add_page()
                    pdf.set_font("Courier", '', 8)
                    pdf.multi_cell(0, 5, page, 0, "L")
                    pdf.output(os.path.join(DIR_ATTACH, vendor +'.pdf'), "F")
        os.rename(os.path.join(DIR_TO_SCAN, f), os.path.join(DIR_ARCHIVE, f))
