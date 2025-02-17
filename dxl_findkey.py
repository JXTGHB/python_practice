import pandas as pd
import xml.etree.ElementTree as ET
import re
import shutil
import os
from lxml import etree
def remove_namespace(tree):
    for elem in tree.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]

def fix_xml_content(content):
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(content, parser=parser)
    return etree.tostring(root, encoding='unicode')

def modify_dxl_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        dxl_content = file.read()
    dxl_content = re.sub(r'<field><field', '<field', dxl_content)
    dxl_content = re.sub(r'</field></field>', '</field>', dxl_content)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(dxl_content)
    print("DXL 文件已成功修改。")

def extract_data(elements, element_name, attrib_name):
    global keyword
    pattern_formula = r"<formula>(.*?)</formula>"
    pattern_lotus = r"<lotusscript>(.*?)</lotusscript>"
    button_name_f = r"/>(.*?)</button>"
    button_name_lo = r"/>(.*?)<code"
    data_list = pd.DataFrame(columns=[attrib_name, 'Formula', 'Flag', 'Event'])
    
    default_data = pd.DataFrame([{attrib_name: 'N/A', 'Formula': 'N/A', 'Flag': 'N/A', 'Event': 'N/A'}])
    data_list = pd.concat([data_list, default_data], ignore_index=True)

    for elem in elements:
        elem_str = ET.tostring(elem, encoding='unicode')
        match_formula = re.search(pattern_formula, elem_str, re.DOTALL)
        match_lotus = re.search(pattern_lotus, elem_str, re.DOTALL)
        code_elem = elem.find(".//code")
        event_value = code_elem.attrib['event'] if code_elem is not None else "No event"
        
        if match_formula:
            content_formula = match_formula.group(1).strip()
        else:
            content_formula = "No formula"
        if match_lotus:
            content_lotus = match_lotus.group(1).strip()
        else:
            content_lotus = "No lotusscript"
        
        #flag = 'Y' if '"ns1"' in content_formula or '"ns1"' in content_lotus else 'N'
        flag = 'Y' if keyword in content_formula or keyword in content_lotus else 'N'
        if element_name == 'button':
            if content_formula == "No formula":
                match_button = re.search(button_name_lo, elem_str, re.DOTALL)
            elif content_lotus == "No lotusscript":
                match_button = re.search(button_name_f, elem_str, re.DOTALL)
            if match_button:
                attribs = elem.attrib
                attribs[attrib_name] = match_button.group(1).strip()
                attribs['Flag'] = flag
                attribs['Event'] = event_value
                attribs['Formula'] = content_formula
                attribs['LotusScript'] = content_lotus
                new_row = pd.DataFrame([attribs])
                data_list = pd.concat([data_list, new_row], ignore_index=True)
                continue
        attribs = elem.attrib
        attribs[attrib_name] = elem.attrib.get('name', elem.attrib.get('title', elem.attrib.get('htmlid', '')))
        attribs['Flag'] = flag
        attribs['Event'] = event_value
        attribs['Formula'] = content_formula
        attribs['LotusScript'] = content_lotus
        new_row = pd.DataFrame([attribs])
        data_list = pd.concat([data_list, new_row], ignore_index=True)
    
    return data_list

def process_dxl_file(input_file, output_file, is_agent_file, is_page_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    remove_namespace(root)
    
    if is_agent_file or is_page_file:
        code_elements = root.findall(".//code")
        code_list = extract_data(code_elements, 'code', 'CodeName')
        flag_column = code_list['Flag']
    else:
        field_list = extract_data(root.findall(".//field[@type]"), 'field', 'FieldName')
        action_list = extract_data(root.findall(".//action[@title]"), 'action', 'ActionTitle')
        actionhotspot_list = extract_data(root.findall(".//actionhotspot[@hotspotstyle]"), 'actionhotspot', 'ActionHotspotTitle')
        area_list = extract_data(root.findall(".//area[@type]"), 'area', '焦點資訊名稱')
        button_list = extract_data(root.findall(".//button"), 'button', 'ButtonName')
        flag_column = pd.concat([field_list['Flag'], action_list['Flag'],actionhotspot_list['Flag'], area_list['Flag'], button_list['Flag']])

    if 'Y' in flag_column.values:
        match = re.search(r'fixed_(.*?)_process\.dxl', input_file)
        extracted_filename = match.group(1)
        with open('result.txt', 'a', encoding='utf-8') as result_file:
            result_file.write(f"檔案 {extracted_filename} 包含 flag 為 'Y' 的欄位。\n")    

    
    with pd.ExcelWriter(output_file) as writer:
        if is_agent_file or is_page_file:
            code_list.to_excel(writer, sheet_name='Code', index=False)
        else:
            field_list.to_excel(writer, sheet_name='Fields', index=False)
            action_list.to_excel(writer, sheet_name='Actions', index=False)
            actionhotspot_list.to_excel(writer, sheet_name='ActionHotspots', index=False)
            area_list.to_excel(writer, sheet_name='Area', index=False)
            button_list.to_excel(writer, sheet_name='Buttons', index=False)
    
    #tree.write('modified_' + input_file, encoding='unicode')
    #modify_dxl_file('modified_' + input_file, 'modified_' + input_file)

def process_dxl_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.dxl'):
            input_file = os.path.join(directory, filename)
            with open(input_file, 'r', encoding='big5', errors='ignore') as file:
                dxl_content = file.read()

            fixed_dxl_content = fix_xml_content(dxl_content)

            fixed_file = os.path.join(directory, 'fixed_' + filename)
            with open(fixed_file, 'w', encoding='utf-8') as file:
                file.write(fixed_dxl_content)

            # Copy the fixed DXL file to a new file with _process suffix
            process_file = fixed_file.replace('.dxl', '_process.dxl')
            shutil.copy(fixed_file, process_file)

            is_agent_file = "Agents" in filename or "ScriptLibraries" in filename
            is_page_file = "Pages" in filename

            # Process the copied DXL file
            output_file = os.path.join(directory, filename.replace('.dxl', '.xlsx'))
            process_dxl_file(process_file, output_file, is_agent_file, is_page_file)
            print(f"已處理 {filename}，輸出檔案為 {output_file}。")

def delete_fixed_files(directory):
    for filename in os.listdir(directory):
        if filename.startswith('fixed_'):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"已刪除文件: {file_path}")
            except Exception as e:
                print(f"刪除文件失敗: {file_path}, 錯誤: {e}")

                
# Specify the directory containing the DXL files
keyword = input("請輸入要搜尋的關鍵字：")
with open('result.txt', 'w', encoding='utf-8') as result_file:
        result_file.write('')    
directory = os.path.dirname(os.path.abspath(__file__))  #py用這個
#directory = os.getcwd()  #ipy用這個
process_dxl_files_in_directory(directory)
delete_fixed_files(directory)
print("所有 DXL 檔案已處理完成。")
# input_file = 'test.dxl'
# with open(input_file, 'r') as file:
#     dxl_content = file.read()

# fixed_dxl_content = fix_xml_content(dxl_content)

# fixed_file = 'fixed_' + input_file
# with open(fixed_file, 'w', encoding='utf-8') as file:
#     file.write(fixed_dxl_content)

# # Copy the fixed DXL file to a new file with _process suffix
# process_dxl_file('SubForms_($WFlowControl).dxl', 'output.xlsx')
