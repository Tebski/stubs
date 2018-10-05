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
                print("Empty page")
                pages.pop()

            for page in pages:
                #print(page)
                venindex = page.find("Ven: ")
                if venindex == -1:
                    print("no vendor found in " + f)
                else:
                    vendor = page[venindex+5:venindex+11].strip()
                    print("Processing vendor: " + vendor)
                    page = page[page.find('\n')+1:] #suppress first line
                    pdf = FPDF(format="letter")
                    pdf.add_page()
                    pdf.set_font("Courier",'',8)
                    pdf.multi_cell(0,5,page,0,"L")
                    pdf.output(os.path.join(dir_attach,vendor +'.pdf'),"F")
        os.rename(os.path.join(dir_to_scan,f),os.path.join(dir_archive,f))
        #if (f.endswith(".txt")):
