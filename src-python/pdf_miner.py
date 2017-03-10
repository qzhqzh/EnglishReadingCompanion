# -*- coding: utf-8 -*-   
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import os
# os.chdir(r'F:\test')
fp = open('coli_a_00261.pdf', 'rb')
#������һ��pdf�ĵ�������
parser = PDFParser(fp)  
#����һ��PDF�ĵ�����洢�ĵ��ṹ
document = PDFDocument(parser)
# ����ļ��Ƿ������ı���ȡ
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
else:
    # ����һ��PDF��Դ�������������洢������Դ
    rsrcmgr=PDFResourceManager()
    # �趨�������з���
    laparams=LAParams()
    # ����һ��PDF�豸����
    # device=PDFDevice(rsrcmgr)
    device=PDFPageAggregator(rsrcmgr,laparams=laparams)
    # ����һ��PDF����������
    interpreter=PDFPageInterpreter(rsrcmgr,device)
    # ����ÿһҳ
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # ���ܸ�ҳ���LTPage����
        layout=device.get_result()
        for x in layout:
            if(isinstance(x,LTTextBoxHorizontal)):
                with open('a.txt','a') as f:
                    f.write(x.get_text().encode('utf-8')+'\n')