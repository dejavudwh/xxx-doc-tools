import pdfplumber
import pandas as pd
import re
import difflib

def comapre_pdf_table(pdf_path, excel_path, page_number):
    result = []
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        tables = page.extract_tables()
        for table in tables:
            for index, row in enumerate(table):
                headers = table[0]
                if index == 0:
                    if not isParamsTable(headers):
                        break
                    else:
                        continue
                pdf_row = arrange_pdf_row(headers, row)
                excel_row = arrange_excel_row(excel_path, pdf_row[0])
                similarity = compare_row(pdf_row, excel_row)
                result.append(pdf_row)
                result.append(excel_row)
                result.append(similarity)
    return result

def isParamsTable(headers):
    # (参数 || 功能码) & (功能定义 || 参数说明 || 设定说明 || 默认值 || 设定值 || 设定范围）
    print('分析是否是参数表')
    print(headers)
    param = False
    other = False
    for col in headers:
        if col in ['参数', '功能码']:
            param = True
        elif col in ['参数名称', '功能定义', '参数说明', '设定说明', '默认值', '设定值', '设定范围']:
            other = True

    return param and other

def arrange_pdf_row(headers, row):
    new_row = [''] * 5
    for i, h in enumerate(headers):
        if h in ['参数', '功能码']:
            new_row[0] = row[i]
        elif h in ['参数名称', '功能定义']:
            new_row[1] = row[i]
        elif h in ['默认值', '出厂值']:
            new_row[2] = row[i]
        elif h in ['设定值', '设定范围']:
            new_row[3] = re.sub(r'[\n\t\r]', '', row[i])
        elif h in ['设定说明', '参数说明']:
            new_row[4] = re.sub(r'[\n\t\r]', '', row[i])
    
    print('重新排布pdf row')
    print(new_row)
    return new_row

def arrange_excel_row(excel_path, param):
    new_row = [''] * 6
    sheet_name = 'Sheet1' 
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    columns_to_extract = ['参数', '参数名称', '设定值', '设定说明', '最小值', '最大值', '出厂值', '单位']
    filtered_df = df[df['参数'] == param]
    extracted_data = filtered_df[columns_to_extract]
    for _, row in extracted_data.iterrows():
        new_row[0] = row['参数']
        new_row[1] = row['参数名称']
        new_row[2] = "{}{}".format(row['出厂值'], row['单位'])
        new_row[3] = "{}{}~{}{}".format(row['最小值'], row['单位'], row['最大值'], row['单位'])
        new_row[4] = re.sub(r'[\n\t\r]', '', row['设定说明'])
        # track
        new_row[5] = re.sub(r'[\n\t\r]', '', str(row['设定值']))
    
    print('重新排布excel row')
    print(new_row)
    return new_row

def compare_row(pdf_row, excel_row):
    ss = []
    for index, element in enumerate(pdf_row):
        similarity = 0.0
        if element != '':
            similarity = difflib.SequenceMatcher(None, element, excel_row[index]).ratio()
            if index == 3:
                s2 = difflib.SequenceMatcher(None, element, excel_row[5]).ratio()
                if (s2 > similarity):
                    excel_row[3] = excel_row[3] + ' + ' + excel_row[5]
                    similarity = max(similarity, s2)

        ss.append(similarity)
    
    print("ss:")
    print(ss)
    return ss