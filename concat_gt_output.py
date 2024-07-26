import os
import json
import pdb

def merge_each_file_with_main(main_file, folder_path, output_folder):
    # 读取主 JSON 文件
    
    # 遍历文件夹中的所有 JSON 文件并合并内容
    for filename in os.listdir(folder_path):
        with open(main_file, 'r', encoding='utf-8') as main_f:
            main_data = json.load(main_f)
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                temp_data = json.load(f)
                merged_data = main_data.copy()  # 创建主数据的副本
                
                for key in temp_data:
                    if key in merged_data:
                        # 合并内容
                        merged_data[key].update(temp_data[key])
                    else:
                        # 将新条目添加到合并数据中
                        merged_data[key] = temp_data[key]

            # 保存合并后的 JSON 数据到新的文件
            output_file_path = os.path.join(output_folder, f"merged_{filename}")
            with open(output_file_path, 'w', encoding='utf-8') as out_f:
                json.dump(merged_data, out_f, ensure_ascii=False, indent=4)
            print(f"Merged file saved to {output_file_path}")

# 示例路径（请替换为实际路径）
main_json_file = 'input/task2/gt_task2_2024-05-30_test.json'
json_folder = 'result/test_output/task2/reason_noTiTou_reasonY'
output_folder = 'result/test_output_gt/task2/reason_noTiTou_reasonY'

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 合并 JSON 文件
merge_each_file_with_main(main_json_file, json_folder, output_folder)
