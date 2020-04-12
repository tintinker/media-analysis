import sys
import os
import io
import re
from sys import argv, exit


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import enchant


def convert_pdf_to_txt(path):
    '''
    Effectively runs pdf2txt.py with default artguments
    See 'pdf2txt.py' in the pdfminer script directory for details
    '''

    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pagenos = set()

    fp = open(path, 'rb')
    for page in PDFPage.get_pages(fp, pagenos):
        interpreter.process_page(page)

    fp.close()
    device.close()

    text = retstr.getvalue()
    return text


def guess_text(text):
    '''
    Tries to get rid of header/footer text from pdfs
    TODO: optimize for more article styles
    '''

    if not text:
        return None

    #one known article style begins relavent text with FULL TEXT and starts footer at DETAILS
    ft,ds = text.find('FULL TEXT'), text.find('DETAILS')
    if ft != -1 and ds != -1 and ft < ds:
        return text[ft + len('FULL TEXT'):ds]

    return text

def fix_text(text):
    '''
    Common issue with PDF to text is words getting broken up by spaces.
    Leverages enchant's spell check to try to identify and put back together these words
    '''

    fixed_text = ''
    words = text.split(' ')
    #reverse loop to account for changing length when words are combined
    for i in range(len(words) - 1, -1, -1):
        try:
            #ex. T uesday -> Tuesday or y ellow -> yellow
            if i > 0 and not english.check(words[i]) and english.check(words[i-1] + words[i]):
                words[i - 1] += words[i]
                continue
        except Exception as e:
            #enchant complains when you give it an empty string, and for a few other unknown reasons
            #if enchant can't process the word, we won't try to combine it
            print(e)

        fixed_text = words[i] + ' ' + fixed_text
    return fixed_text

if __name__ == '__main__':
    if len(argv) != 2 or argv[1] in ['-h', '--help']:
        print("usage: textify.py [PATH TO FOLDER]")
        print("ex. textify.py ./articles/2018/byrace/B")

    base_path = argv[1]

    #note: may need to install enchant C libraries with brew install enchant
    english = enchant.Dict("en_US")

    #grab all PDF files in directory and subdirectories
    filelist = []
    for dirpath,_,filenames in os.walk(base_path):
        for filename in filenames:
            if filename.endswith('.pdf'):
                filelist.append(os.path.join(dirpath,filename))

    for file in filelist:
        print(f"Converting file: {file}")

        #in Ryzdik's naming format, the foldername is the same as the victim's name
        #we want victim's first/last/middle name to pass spell check
        for name_word in re.split(' |_', os.path.basename(os.path.dirname(file))):
          english.add(name_word)

        #grab text with a few optimizations (combining words & locating start/end of full text)
        text = guess_text(fix_text(convert_pdf_to_txt(file)))

        #write to text file with same name
        with open(file[:-3] + 'txt',"w+") as f:
            f.write(text)
