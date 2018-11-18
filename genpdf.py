'''
Script to process .txt files from glovia, and convert to PDF
Version 1.4 - SRE
Store pages without a vendor to be collated with a page that has a vendor to handle
scenario of vendor with multiple pages of stubs

Version 1.3 - SRE
Removed assumption on CODIV being MDC. Search now only looks for the report function
name to find the page headers.

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

ATTACH_SUB_DIR = 'attachments'
ARCHIVE_SUB_DIR = 'archive'
TXT_SUB_DIR = 'text'
HOME_DIR = os.path.curdir
DIR_TO_SCAN = os.path.join(HOME_DIR, TXT_SUB_DIR)
DIR_ARCHIVE = os.path.join(HOME_DIR, ARCHIVE_SUB_DIR)
DIR_ATTACH = os.path.join(HOME_DIR, ATTACH_SUB_DIR)


print("Scanning: " + DIR_TO_SCAN)
def main():
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
            #print(idate)
            with open(os.path.join(DIR_TO_SCAN, f), "r") as ifile:
                txt = ifile.read()
                
                #check if it contains multiple pages
                if txt.count('C_ACHSTB') > 1:
                    #multiple headers found
                    if txt.count('\f') == 0:
                        #no page breaks found, need to insert them
                        start = 10 #ignore first occurence
                        pos = 1
                        while pos < len(txt) and pos > 0:
                            pos = (txt.find('C_ACHSTB', start))
                            #print("position: " + str(pos))
                            if pos > -1:
                                txt = txt[:pos-6] + '\f' + txt[pos-5:]
                                start = pos+1

                #split on page break
                pages = txt.split("\f")
                #remove last page (if it's blank)
                if len(pages[-1].strip()) == 0:
                    print("Empty page being ignored")
                    pages.pop()

                ven_pages = []

                for page in pages:
                    page = page[page.find('\n')+1:] #suppress first line
                    venindex = page.find("Ven: ")
                    if venindex == -1:
                        ven_pages.append(page)
                        print("multipage vendor found")
                    else:
                        vendor = page[venindex+5:venindex+11].strip()
                        if not vendor:
                            print("Invalid vendor found in " + f)
                        else:
                            print("Processing vendor: " + vendor)
                            ven_pages.append(page)
                            pdf = FPDF(format="letter")
                            for ven_page in ven_pages:
                                pdf.add_page()
                                pdf.set_font("Courier", '', 8)
                                pdf.multi_cell(0, 4, ven_page, 0, "L")
                            pdf.output(os.path.join(DIR_ATTACH, vendor + "_" + idate + '.pdf'), "F")
                            ven_pages.clear()
            try:
                os.rename(os.path.join(DIR_TO_SCAN, f), os.path.join(DIR_ARCHIVE, f))
            except FileExistsError as e:
                print("File " + f + " already exists in " + DIR_ARCHIVE + ". Attempting cleanup.")
                os.remove(os.path.join(DIR_ARCHIVE, f))
                os.rename(os.path.join(DIR_TO_SCAN, f), os.path.join(DIR_ARCHIVE, f))

        else:
            print("Invalid file name " + f + " found in " + DIR_TO_SCAN)


if __name__ == '__main__':
    main()
