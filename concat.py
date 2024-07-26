import os
import json
import pandas as pd

# 设定目录路径
dir_path = 'test_output/no-reason'

# 初始化一个空的DataFrame
df = pd.DataFrame()

# 遍历目录中的所有JSON文件
for file_name in os.listdir(dir_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(dir_path, file_name)
        
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 初始化临时字典来保存当前文件的数据
        temp_data = {'ID': [], file_name: []}
        
        # 提取数据，根据具体的JSON结构进行分支处理
        for key, value in data.items():
            temp_data['ID'].append(key)
            if '子事件' in value:
                temp_data[file_name].append(value.get('子事件', '').replace('\n', ' '))
            elif '输出结果' in value:
                output_result = value.get('输出结果', [''])[0]
                output_result = output_result.replace("核电厂始发事件子事件分析人员：", "").replace("\n", " ")
                temp_data[file_name].append(output_result)
            else:
                temp_data[file_name].append('')
        
        # 将临时数据的字典转换为DataFrame
        temp_df = pd.DataFrame(temp_data)
        
        # 合并到主DataFrame中
        if df.empty:
            df = temp_df
        else:
            df = pd.merge(df, temp_df, on='ID', how='outer')

# 保存为Excel文件
df.to_excel('output.xlsx', index=False)

print("数据已成功保存到output.xlsx")
