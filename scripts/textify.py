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

if len(argv) != 2:
    print("usage: textify.py [PATH TO FOLDER]")
    print("ex. textify.py ./articles/2018/byrace/B")

english = enchant.Dict("en_US")

#foldername = sys.argv[1]
filelist = []



def convert_pdf_to_txt(path):
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
    if not text:
        return None

    ft,ds = text.find('FULL TEXT'), text.find('DETAILS')
    if ft != -1 and ds != -1 and ft < ds:
        return text[ft + len('FULL TEXT'):ds]

    return text

def fix_text(text):
    fixed_text = ''
    words = text.split(' ')
    for i in range(len(words) - 1, -1, -1):
        try:
            if i > 0 and not english.check(words[i]) and english.check(words[i-1] + words[i]):
                words[i - 1] += words[i]
                continue
        except Exception as e:
            #error with enchant library, don't try to fix word
            print(e)

        fixed_text = words[i] + ' ' + fixed_text
    return fixed_text

for dirpath,_,filenames in os.walk(argv[1]):
    for filename in filenames:
        if filename.endswith('.pdf'):
            filelist.append(os.path.join(dirpath,filename))

for file in filelist:
    print(f"Converting file: {file}")

    for name_word in re.split(' |_', os.path.basename(os.path.dirname(file))):
      english.add(name_word)

    text = guess_text(fix_text(convert_pdf_to_txt(file)))

    with open(file[:-3] + 'txt',"w+") as f:
        f.write(text)
