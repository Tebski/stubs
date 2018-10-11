import os

dir_to_scan = os.path.join(os.path.curdir,"stubs")
files = os.listdir(dir_to_scan)

for f in files:
    bdateindex = f.find("ACHStubs_")
    edateindex = f.find(".txt")
    idate = f[bdateindex+9:edateindex]
    print(idate)

    with open(os.path.join(dir_to_scan,f),"r") as ifile:
        txt = ifile.read()
        #look for page break
        #pb = txt.find()
        #print(txt)
        pages = txt.split("\f")
        print(len(pages))
        ofilepath = os.path.join(dir_to_scan,vendor + "_ACHStubs_" + idate + ".txt")

        with open(ofilepath,"w") as ofile:
            ofile.write(pages[i])
