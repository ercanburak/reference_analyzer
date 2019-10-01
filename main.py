import os
import re
import PyPDF2

path = '/home/gg/.local/share/data/Mendeley Ltd./Mendeley Desktop/Downloaded/'
txt = ''

def find_ref_number(pdftext, pos):
    refnum = 0
    for i in range(50):
        tmp_pos = pos-i
        if(pdftext[tmp_pos] == '['):
            if(pdftext[tmp_pos+2] == ']'):
                refnum = pdftext[tmp_pos+1]
            elif(pdftext[tmp_pos+3] == ']'):
                refnum = pdftext[tmp_pos+1:tmp_pos+3]
            elif(pdftext[tmp_pos+4] == ']'):
                refnum = pdftext[tmp_pos+1:tmp_pos+4]
            break
    return refnum

def valid_ref(pdftext, pos, refnum):
    if(pdftext[pos-1].isdigit()):
        return False
    if(pdftext[pos+len(refnum)].isdigit()):
        return False
    for i in range(10):
        if(pdftext[pos-i] == '['):
            for j in range(10):
                if(pdftext[pos+j] == ']'):
                    return True
    return False

def purify_occurences(pdftext, occurences, refnum):
    occs = []
    for occ in occurences:
        if(valid_ref(pdftext, occ, refnum)):
            occs.append(occ)
    return occs

def get_sentence_pos(pdftext, pos):
    flag = False
    for i in range(300):
        if(pdftext[pos-i] == '.'):
            if(flag):
                flag = False
                for j in range(300):
                    if(pdftext[pos+j] == '.'):
                        if(flag):
                            break
                        else:
                            flag = True
                break
            else:
                flag = True
    return [pos-i,pos+j]

def print_ref(pdftext, occurences, file, refnum):
    for occ in occurences:
        [start, end] = get_sentence_pos(pdftext, occ)
        txt+='********************************\n'
        txt+=file + ':' + refnum + '\n'
        txt+='-------------------\n'
        txt += pdfstr[start:end] + '\n'
        txt+='-------------------\n'
        print(txt)

papers = []
for r, d, f in os.walk(path):
    for file in f:
        if '.pdf' in file:
            tmp = [m.start() for m in re.finditer('-', file)]
            tmpstr = file[tmp[1]+2:]
            tmpstr = tmpstr.replace('.pdf', '')
            tmpstr = tmpstr.replace(' ', '')
            tmpstr = tmpstr.lower()
            papers.append(tmpstr)

for paper in papers:
    txt = ''
    file1 = open(paper + '.txt',"w") 
    name =  paper
    for r, d, f in os.walk(path):
        for file in f:
            if '.pdf' in file:
                try:
                    pdfFileObj = open(os.path.join(r, file), 'rb')
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                    pdfstr = ""
                    for i in range(pdfReader.numPages):
                        pdfstr += pdfReader.getPage(i).extractText().lower()
                    pdfstr = pdfstr.replace('\n', '')
                    if(pdfstr.find(name) != -1):
                        refnum = find_ref_number(pdfstr, pdfstr.find(name))
                        if(refnum != 0):
                            occurences = [m.start() for m in re.finditer(refnum, pdfstr)]
                            occurences = purify_occurences(pdfstr, occurences, refnum)
                            print_ref(pdfstr, occurences, file, refnum)
                    del pdfFileObj, pdfReader, pdfstr
                except:
                    print('exception')
    file1.write(txt) 
    file1.close()