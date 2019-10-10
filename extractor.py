import sys
import os
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from io import StringIO
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
import PyPDF2

class MyParser(object):
    def __init__(self, pdf):
        ## Snipped adapted from Yusuke Shinyamas 
        #PDFMiner documentation
        # Create the document model from the file
        parser = PDFParser(open(pdf, 'rb'))
        document = PDFDocument(parser)
        # Try to parse the document
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # Create a PDF resource manager object 
        # that stores shared resources.
        rsrcmgr = PDFResourceManager()
        # Create a buffer for the parsed text
        retstr = StringIO()
        # Spacing parameters for parsing
        laparams = LAParams()
        codec = 'utf-8'
 
        # Create a PDF device object
        device = TextConverter(rsrcmgr, retstr, 
                               codec = codec, 
                               laparams = laparams)
        # Create a PDF interpreter object
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
         
        self.records            = []
        self.txt = ''
         
        lines = retstr.getvalue().splitlines()
        for line in lines:
            self.handle_line(line)
     
    def handle_line(self, line):
        # Customize your line-by-line parser here
        self.records.append(line)
        line = line.replace('ﬁ', 'fi')
        if(line.endswith('-')):
            self.txt += line.lower().replace('-', '')
        elif(not line.endswith(' ')):
            self.txt += line.lower() + ' '


if __name__ == '__main__':
    path = '/home/gg/.local/share/data/Mendeley Ltd./Mendeley Desktop/Downloaded/'
    papers = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.pdf' in file:
                tmp = [m.start() for m in re.finditer('-', file)]
                paper = file[tmp[1]+2:]
                paper = paper.replace('.pdf', '')
                paper = paper.lower()
                #papers.append(paper)

                if(not os.path.isfile('textedpdfs/miner/' + paper + '.txt')):
                    p = MyParser(os.path.join(r, file))
                    with open('textedpdfs/miner/' + paper + '.txt',"w")  as filetxt:
                        filetxt.write(p.txt) 
                    del p

                if(not os.path.isfile('textedpdfs/pypdf/' + paper + '.txt')):
                    pdfFileObj = open(os.path.join(r, file), 'rb')
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                    pdfstr = ""
                    if(pdfReader.numPages < 50):
                        for i in range(pdfReader.numPages):
                            pdfstr += pdfReader.getPage(i).extractText().lower()
                        pdfstr = pdfstr.replace('\n', '')                    
                        with open('textedpdfs/pypdf/' + paper + '.txt',"w")  as filetxt:
                            filetxt.write(pdfstr) 
                    pdfFileObj.close()
                    del pdfReader
