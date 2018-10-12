'''
Script to process .txt files from glovia, and convert to PDF

Version 1.2 - SRE
Added ability to split txt file based on vendor, as page breaks from the text
file appear unreliable
Suppress first line as it contains a page number which could be confusing to the end user
Modified script to run from the /stubs/ folder.

Version 1.1 - SRE
Separated files into subfolders to make directory cleaner.
Removed last page if its blank to prevent empty pdfs being created

Version 1.0 - SRE
Agnes Evans Consulting. For inquiries call +1 310 294 3639.

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
import os

attach_sub_dir = 'attachments'
archive_sub_dir = 'archive'
txt_sub_dir = 'text'
home_dir = os.path.join(os.path.curdir,"stubs")
dir_to_scan = os.path.join(home_dir,txt_sub_dir)
dir_archive = os.path.join(home_dir,archive_sub_dir)
dir_attach = os.path.join(home_dir,attach_sub_dir)
files = os.listdir(dir_to_scan)
valid_file = True




# Process files
for f in files:
    print("processing: " + f)
    bdateindex = f.find("ACHStubs_")
    edateindex = f.find(".txt")

    if edateindex == -1 or bdateindex == -1:
        #print("No .txt file extension on this one")
        valid_file = False
    else:
        valid_file = True

    if valid_file:
        idate = f[bdateindex+9:edateindex]
        print(idate)
        with open(os.path.join(dir_to_scan,f),"r") as ifile:
            txt = ifile.read()
            #print(txt)
            #check if it contains multiple pages
            if txt.count('MDC  C_ACHSTB') > 1:
                #multiple headers found
                if txt.count('\f') == 0:
                    #no page breaks found, need to insert them
                    start = 10 #ignore first occurence
                    pos = 1
                    while pos < len(txt) and pos > 0:
                        pos = txt.find('MDC  C_ACHSTB',start)
                        if pos > -1:
                            txt = txt[:pos-1] + '\f' + txt[pos:]
                            start = pos+1

            #split on page break
            pages = txt.split("\f")
            #remove last page (if it's blank)
            if len(pages[-1].strip()) == 0:
                print("Empty page being ignored")
                pages.pop()

            for page in pages:
                #print(page)
                venindex = page.find("Ven: ")
                if venindex == -1:
                    print("no vendor found in " + f)
                else:
                    vendor = page[venindex+5:venindex+11].strip()
                    if not vendor:
                        print("Invalid vendor found in " + f)
                    else:
                        print("Processing vendor: " + vendor)
                        page = page[page.find('\n')+1:] #suppress first line
                        pdf = FPDF(format="letter")
                        pdf.add_page()
                        pdf.set_font("Courier", '', 8)
                        pdf.multi_cell(0, 5, page, 0, "L")
                        pdf.output(os.path.join(DIR_ATTACH, vendor + "_" + idate + '.pdf'), "F")
        os.rename(os.path.join(DIR_TO_SCAN, f), os.path.join(DIR_ARCHIVE, f))
    else:
        print("Invalid file name " + f + " found in " + DIR_TO_SCAN)
