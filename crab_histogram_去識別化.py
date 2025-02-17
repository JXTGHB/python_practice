import gzip
import shutil
import os
import re
import json
import zipfile
import rarfile
import cx_Oracle
import subprocess
from datetime import datetime

def unzip_gz_file(gz_file_path, extract_to_dir):
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)
    
    file_name = os.path.basename(gz_file_path)
    output_file_path = os.path.join(extract_to_dir, os.path.splitext(file_name)[0])
    
    with gzip.open(gz_file_path, 'rb') as f_in:
        with open(output_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            #print(f"文件 {gz_file_path} 已解壓縮到 {output_file_path}")

def unzip_zip_file(zip_file_path, extract_to_dir):
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)
        print(f"文件 {zip_file_path} 已解壓縮到 {extract_to_dir}")

def unzip_rar_file(rar_file_path, extract_to_dir):
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)
    
    if rarfile.is_rarfile(rar_file_path):
        with rarfile.RarFile(rar_file_path, 'r') as rar_ref:
            rar_ref.extractall(extract_to_dir)
            print(f"文件 {rar_file_path} 已解壓縮到 {extract_to_dir}")
    else:
        print(f"錯誤: 文件 {rar_file_path} 不是有效的 RAR 文件")

def unzip_rar_with_7zip(rar_file_path, extract_to_dir):
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)

    try:
        # 呼叫 7-Zip 來解壓縮 RAR 檔案
        subprocess.run(['7z', 'x', rar_file_path, f'-o{extract_to_dir}'], check=True)
        print(f"文件 {rar_file_path} 已成功解壓縮到 {extract_to_dir}")
    except subprocess.CalledProcessError as e:
        print(f"解壓縮失敗: {e}")
    except FileNotFoundError:
        print("找不到 7-Zip 可執行檔，請確認 7-Zip 已正確安裝並加入系統路徑。")

def unzip_all_gz_files_in_folder(folder_path):
    extract_to_dir = os.path.join(folder_path, 'unzip')
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)
        
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.gz'):
            unzip_gz_file(file_path, extract_to_dir)
        elif filename.endswith('.zip'):
            unzip_zip_file(file_path, extract_to_dir)
        elif filename.endswith('.rar'):
            unzip_rar_file(file_path, extract_to_dir)
        elif filename.endswith('.hst'):
            destination_path = os.path.join(extract_to_dir, filename)
            
            with open(file_path, 'r') as src_file:
                content = src_file.read()
            
            with open(destination_path, 'w') as dest_file:
                dest_file.write(content)
    # for filename in os.listdir(folder_path):
    #     if filename.endswith('.gz'):
    #         gz_file_path = os.path.join(folder_path, filename)
    #         extract_to_dir = os.path.join(folder_path, 'unzip')
    #         unzip_gz_file(gz_file_path, extract_to_dir)

def extract_hst_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    # 提取 Plan Name
    plan_name_match = re.search(r'Plan Name\s*:\s*(\S*)', content)
    plan_name = plan_name_match.group(1).strip() if plan_name_match else 'N/A'
    date_match = re.search(r'Date:\s*(.*)', content)
    date_str = date_match.group(1).strip()
    date_obj = datetime.strptime(date_str, "%b %d %H:%M %Y")
    format_date = date_obj.strftime("%Y/%m/%d %H:%M")
    
    # 提取每個Item 的 Pass Count
    #item_data = re.findall(r'Item No:\s*(\d+).*?Pass Count\s*:\s*(\d+)', content, re.DOTALL)
    item_data = re.findall(r'Item No:\s*(\d+).*?Pass Count\s*:\s*(\d+).*?Test ID:\s*(\d+)', content, re.DOTALL)
    
    return plan_name, item_data,format_date

def read_hst_files_in_folder(folder_path):
    #create json folder
    #json_folder_path = os.path.join(folder_path, 'json')
    #if not os.path.exists(json_folder_path):
    #    os.makedirs(json_folder_path)

    #all_data = []
    hst_files = [filename for filename in os.listdir(folder_path) if filename.endswith('.hst')]
    if not hst_files:
        print(f"錯誤: 資料夾 {folder_path} 中沒有 .hst 檔案")

    processed_folder = os.path.join(current_dir, '已處理_無異常')
    result_folder = os.path.join(current_dir, 'result')
    
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith('.hst'):
            print(f"Reading file: {filename}")
            hst_file_path = os.path.join(folder_path, filename)
            plan_name, item_data,testdate = extract_hst_data(hst_file_path)

            lotname_match = re.match(r'([^_]+)', filename)
            waferno_match = re.search(r'-(\d+)', filename)
            lotname = lotname_match.group(1) if lotname_match else 'N/A'
            waferno = waferno_match.group(1) if waferno_match else 'N/A'
            
            print(f"Plan Name: {plan_name}")
            print(f"Lot Name: {lotname}")
            print(f"Wafer No: {waferno}")
            print(f"Test Date: {testdate}")

            #items = [{"Item No": item_no, "Pass Count": pass_count} for item_no, pass_count in item_data]
            items = [{"Item No": item_no, "Pass Count": pass_count,"Test ID":test_id} for item_no, pass_count,test_id in item_data]
            
            # 產生 JSON 檔案
            # file_data = ({
            #     "Plan Name": plan_name,
            #     "Lot Name": lotname,
            #     "Wafer No": waferno,
            #     "Items": items
            # })
            # json_output_path = os.path.join(json_folder_path, f"{os.path.splitext(filename)[0]}.json")
            # with open(json_output_path, 'w', encoding='utf-8') as json_file:
            #     json.dump(file_data, json_file, ensure_ascii=False, indent=4)
            # print(f"已保存到 {json_output_path}")
            
            if query_oracle_db(filename,plan_name, lotname, waferno, items, testdate):
               move_file(hst_file_path, result_folder)
            else:    
               move_file(hst_file_path, processed_folder)

def move_file(src, dst_folder):
    dst = os.path.join(dst_folder, os.path.basename(src))
    if os.path.exists(dst):
        os.remove(dst)
    shutil.move(src, dst)

def clear_tmp_table():
    dsn_tns = cx_Oracle.makedsn('192.168.xxx.xx', '9999', service_name='xxxxxxx')
    username = 'xxxxx'
    password = 'xxxxx'

    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        print("成功連線到Oracle DB")

        cursor = connection.cursor()

        delete_query = "DELETE FROM T_TANGO_CP_TEST_MAPPING"
        cursor.execute(delete_query)
        connection.commit()
        print("已刪除 TMP TABLE 中的所有項目")

    except cx_Oracle.DatabaseError as e:
        print(f"連線失敗: {e}")
        raise
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
            print("連線已關閉")

def query_oracle_db(filename,plan_name, lotname, waferno, items,testdate):
    dsn_tns = cx_Oracle.makedsn('192.168.xxx.xx', '9999', service_name='xxxxxxx')
    username = 'xxxxx'
    password = 'xxxxx'

    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        print("成功連線到Oracle DB")

        cursor = connection.cursor()

        plan_name_without_tdl = plan_name.replace('.tdl', '')

        query = """
            SELECT TESTPROGRAM, WO_LOT_NO, WAF_NO, TOTAL_CNT, PASS_CNT, RWK_FLAG
            FROM I_TANGO_WAFER_MEASURE_ALL
            WHERE CATEGORY_ID = '1'
              AND WO_LOT_NO = :lotname
              AND OP_NAME LIKE 'CP%'
              AND COMPANY IN ('SITRONIX','STCN')
              AND (TESTPROGRAM = :plan_name_without_tdl OR TESTPROGRAM = :plan_name)
              AND WAF_NO = :waferno
              AND TO_DATE(:testdate, 'yyyy/MM/dd HH24:MI') BETWEEN ST_TIME AND END_TIME
            ORDER BY WAF_NO, RWK_FLAG
        """
        print(lotname, plan_name, waferno)
        #cursor.execute(query, {'lotname': lotname, 'plan_name': plan_name, 'waferno': waferno})
        cursor.execute(query, {'lotname': lotname,'plan_name_without_tdl': plan_name_without_tdl, 'plan_name': plan_name, 'waferno': waferno, 'testdate': testdate})

        # 获取查询结果
        results = cursor.fetchall()
        inserted_any = False
        #print(query)
        #print(results)
        for row in results:
            testprogram, wo_lot_no, waf_no,total_cnt, pass_cnt, rwk_flag = row
            for item in items:
                item_no = item["Item No"]
                item_pass_count = int(item["Pass Count"])
                test_id = item["Test ID"]
                #print(f"Item No: {item_no}, Pass Count: {item_pass_count}, Total Count: {total_cnt}, pass_cnt: {pass_cnt}")
                print(f"要插入的資料: Filename = {filename},TESTPROGRAM={testprogram}, WO_LOT_NO={wo_lot_no}, WAF_NO={waf_no}, ITEM_NO={item_no}, TOTAL_CNT={total_cnt}, ITEM_PASS_COUNT={item_pass_count}, PASS_CNT={pass_cnt}, RWK_FLAG={rwk_flag},TEST_ID={test_id}")
                #if item_pass_count < pass_cnt:
                if item_pass_count < pass_cnt:
                    inserted_any = True
                print(item_pass_count, pass_cnt)
                print(f"符合條件的項目: {row}")
                insert_query = """
                    INSERT INTO T_TANGO_CP_TEST_MAPPING (FILE_NAME,TEST_PG, WO_LOT_NO, WAFER_NO, ITEM_NO, ITEM_PASS_COUNT, PASS_CNT, RWK_FLAG, TEST_ID)
                    VALUES (:filename,:testprogram, :wo_lot_no, :waf_no, :item_no, :item_pass_count, :pass_cnt, :rwk_flag, :test_id)
                """
                cursor.execute(insert_query, {
                    'filename': filename,
                    'testprogram': testprogram,
                    'wo_lot_no': wo_lot_no,
                    'waf_no': waf_no,
                    'item_no': item_no,
                    'item_pass_count': item_pass_count,
                    'pass_cnt': pass_cnt,
                    'rwk_flag': rwk_flag,
                    'test_id': test_id
                })
                connection.commit()
                #inserted_any = True
        return inserted_any
    except cx_Oracle.DatabaseError as e:
        print(f"連線失敗: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
            print("連線已關閉")

#current_dir = os.getcwd()
if __name__ == "__main__":
    current_dir = r"/home/nifiadmin/CP_Code/CP_data_analysis"
    gz_folder = os.path.join(current_dir, 'wait compare')
    # 解壓縮所有文件
    target_folder = os.path.join(gz_folder, 'unzip')
    
    # 如果目標資料夾已存在 先刪除
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)
    os.makedirs(target_folder)

    clear_tmp_table()
    unzip_all_gz_files_in_folder(gz_folder)
    read_hst_files_in_folder(target_folder)