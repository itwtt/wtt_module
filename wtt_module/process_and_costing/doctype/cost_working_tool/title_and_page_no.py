import frappe
from pdfquery import PDFQuery
import fitz 
import PyPDF2
from fpdf import FPDF
@frappe.whitelist()
def page_no(path):
    pdf_path=path
    arr=[]
    pages_to_skip = 0
    pdf_document = fitz.open(pdf_path)
    page_number = 0
    pages_to_skip = 0
    for page in pdf_document:
        page_number += 1
        if page_number <= pages_to_skip:
            continue
        if(page_number in [3,4,5]):
            ar_for_pageskip=[]
            page_text = page.get_text()
            vv = str(page_text.replace(' ','')).lower()
            vs=vv.split()
            for i in vs:
                if('/tcp' in str(i) or 'page|' in str(i) or '..' in str(i) or 'pageno' in str(i)):
                    pass
                else:
                    arr.append(i)
                    ar_for_pageskip.append(i)
            if(len(ar_for_pageskip)>0):
                pages_to_skip=page_number

    page_arr=[]
    ar_for_head_distinct=[]
    for i in arr:
        pdf_path = path
        heading_text = i
        pdf_document = fitz.open(pdf_path)
        page_number = 0
        for page in pdf_document:
            page_number += 1
            if page_number <= pages_to_skip:
                continue
            page_text = page.get_text()
            if heading_text in str(page_text.replace(' ','')).lower():
                if(heading_text not in ar_for_head_distinct):
                    ar_for_head_distinct.append(heading_text)
                    page_arr.append({"heading":heading_text,"page_no":page_number})
    return page_arr


# pdf_file = PyPDF2.PdfReader(open("pp.pdf", "rb"))
# replacements=[]
# for i in range(len(page_arr)):
#     replacements.append(("pageno"+str(int(i)+1),str(page_arr[i]["page_no"])))

# for jj in [2,3]:
#     text = ''
#     page = pdf_file.pages[jj]
#     text = page.extract_text()
#     if(jj==2):
#         for old_text, new_text in replacements:
#             print(str(old_text)+"---------------------------------"+str(new_text))
#             text = text.replace(old_text, new_text)
#     print(text)

