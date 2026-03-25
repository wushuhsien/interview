import pandas as pd
import os

def process_all():
    excel_file = r"C:\interview_ai\position_data\position.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"找不到檔案: {excel_file}，請確認檔案是否在該位置！")
        return

    # 1. 讀取 Excel
    print("正在讀取 Excel...")
    xls = pd.ExcelFile(excel_file)
    all_positions = {}

    # 2. 遍歷每個分頁
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"正在處理分頁: {sheet_name}")

        # 處理每一組職群（每兩欄為一組：職稱, 代碼）
        for i in range(0, df.shape[1], 2):
            category = df.columns[i]
            if pd.isna(category): continue
            
            # 提取職位名稱並清理
            positions_list = df.iloc[:, i].dropna().unique().tolist()
            clean_list = [str(p) for p in positions_list if not str(p).replace('.0','').isdigit()]
            
            if category not in all_positions:
                all_positions[category] = []
            all_positions[category].extend(clean_list)

    # 3. 寫入 positions.py
    output_py = r"C:\interview_ai\positions.py"
    with open(output_py, "w", encoding="utf-8") as f:
        f.write("positions = {\n")
        for cat, pos in sorted(all_positions.items()):
            f.write(f'    "{cat}": {sorted(list(set(pos)))},\n')
        f.write("}\n")
    
    print(f"完成！已產生: {output_py}")

if __name__ == "__main__":
    process_all()