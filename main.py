import os
import re
import PyPDF2
from extractor import extract

pathminer = 'textedpdfs/miner'
pathpy = 'textedpdfs/pypdf'

def find_ref_number(pdftext, pos):
    refnum = 0
    if(pos != -1):
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
    i = j = 0
    for i in range(300):
        if(pdftext[pos-20-i] == '.'):
            if(flag):
                flag = False
                for j in range(300):
                    if(pdftext[pos+20+j] == '.'):
                        if(flag):
                            break
                        else:
                            flag = True
                break
            else:
                flag = True
    return [pos-19-i,pos+20+j]

def print_ref(pdftext, txt, occurences, paper, refnum):
    txt+='********************************' + paper + ' : ' + refnum + '********************************\n'
    for occ in occurences:
        [start, end] = get_sentence_pos(pdftext, occ)
        txt+='-------------------\n'
        txt += pdfstr[start:end].replace('.', '.\n') + '\n'
    return txt

if __name__ == '__main__':
    path2pdfs = '/home/gg/.local/share/data/Mendeley Ltd./Mendeley Desktop/Downloaded/'
    extract(path2pdfs)

    for r, d, f in os.walk(pathminer):
        for file1 in f:
            try:
                paper = file1.replace('.txt', '')
                txt = ''
                for file2 in f:
                    if(file1 != file2):
                        with open(os.path.join(r, file2), 'r') as pdffile:
                            pdfstr = pdffile.read()
                        refnum = find_ref_number(pdfstr, pdfstr.find(paper))
                        if(refnum == 0):
                            if(os.path.isfile(os.path.join(pathpy, file2))):
                                with open(os.path.join(pathpy, file2), 'r') as pdffile:
                                    pdfstr2 = pdffile.read()
                                refnum = find_ref_number(pdfstr2, pdfstr2.find(paper.replace(' ', '')))
                                if(refnum != 0):
                                    print('found in pypdf!!!')

                        if(refnum != 0):
                            occurences = [m.start() for m in re.finditer(refnum, pdfstr)]
                            occurences = purify_occurences(pdfstr, occurences, refnum)
                            txt = print_ref(pdfstr, txt, occurences, file2, refnum)

                    if(txt != ''):
                        with open('citeds/' + paper + '.txt',"w")  as filetxt:  
                            filetxt.write(txt) 
            except Exception as e: 
                print(e)
    
    if(False):
        for r, d, f in os.walk(pathminer):
            for file in f:
                pdffile = open(os.path.join(r, file), 'r')
                pdfstr = pdffile.read()
                pdffile.close()
                pos = pdfstr.find('ﬁ')
                if(pos != -1):
                    pdffile = open(os.path.join(r, file), 'w')
                    pdfstr = pdfstr.replace('ﬁ', 'fi')
                    pdffile.write(pdfstr)