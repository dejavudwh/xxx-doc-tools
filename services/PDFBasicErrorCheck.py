import fitz  # PyMuPDF
import pandas as pd

def basic_error_check(pdf_path, output_path, keywords_and_annot):
    pdf_document = fitz.open(pdf_path)
    for keyword, annotation_text in keywords_and_annot.items():
        print(keyword, annotation_text)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            annot_keywords(page, keyword, annotation_text)

    pdf_document.save(output_path)
    pdf_document.close()

def annot_keywords(page, keyword, annotation_text):
    text_instances = page.search_for(keyword)  
    for inst in text_instances:
        highlight = page.add_highlight_annot(inst)
        highlight.set_colors(stroke=(1, 1, 0))  
        highlight.update()

        rect = fitz.Rect(inst.x0, inst.y0 - 10, inst.x1 + 200, inst.y0)

        annot = page.add_freetext_annot(
                rect,
                annotation_text,
                fontsize=12,
                fontname="china-s", 
                text_color=(1, 0, 0)
        )
        print("批注{}".format(annotation_text))
        annot.update()

def import_item_from_excel(excel_path):
    sheet_name = 'Sheet1' 
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    columns_to_extract = ['匹配', '批注']
    extracted_data = df[columns_to_extract]
    result = []
    for _, row in extracted_data.iterrows():
        match_cond = row['匹配']
        annot = row['批注']
        result.append([match_cond, annot])

    return result