import pandas as pd
import json  # 导入标准库中的json模块
import datetime
import pdb
time_stamp = datetime.datetime.now().strftime("%Y-%m-%d")

# 假设你的Excel文件名为'example.xlsx'
excel_file = 'data_PSA0528.xlsx'
sheet_name = 'Sheet1'  # 替换成你的实际sheet名

task="task2"#task1 识别始发事件; task2 识别操作员动作； task3 事件树题头事件分析
output_name="input/data_"+task+"_"+time_stamp+".json"

gt=True


# 读取Excel文件
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# 要转换成json的列名列表
# columns_to_convert = ['事故类型', '事故描述', '始发事件',	'事件进程和系统响应','操作员动作']

if task=="task1":
    columns_to_convert = ['始发事件', '始发事件描述']
    filtered_df = df[columns_to_convert]

# 去除重复行
    filtered_df = filtered_df.drop_duplicates()
    # 把DataFrame转成字典，准备导出成JSON
    data_to_export = filtered_df.to_dict(orient='index')

    # 将字典转换为我们想要的格式
    final_data = {}
    for idx, (key, value) in enumerate(data_to_export.items(), start=1):
        final_data[str(idx)] = value

    # 导出到JSON文件
    import json
    with open(output_name, 'w', encoding='utf-8') as jsonf:
        json.dump(final_data, jsonf, ensure_ascii=False, indent=4)

    print("JSON文件已生成。")


else:
    if task=="task3":
        columns_to_convert = ['始发事件', '始发事件描述', '子事件','事件进程和系统响应']

        # 初始化结果字典
        result_dict = {}

        # 遍历DataFrame，转换为指定的json格式
        for index, row in df.iterrows():
            result_dict[str(index + 1)] = {
                f"{col}": row[col] if pd.notnull(row[col]) else '' for col in columns_to_convert
            }

        # 将字典转换为JSON格式字符串
        json_str = json.dumps(result_dict, ensure_ascii=False, indent=4)

        # 打印出JSON字符串
        print(json_str)

        # 如果你想把这个JSON字符串保存到文件
        with open(output_name, 'w', encoding='utf-8') as f:
            f.write(json_str)
    if task=="task2":
        columns_to_convert = ['始发事件', '始发事件描述', '子事件','事件进程和系统响应','事件树题头事件']

        # 初始化结果字典
        result_dict = {}

        # 遍历DataFrame，转换为指定的json格式
        for index, row in df.iterrows():
            result_dict[str(index + 1)] = {
                f"{col}": row[col] if pd.notnull(row[col]) else '' for col in columns_to_convert
            }

        # 将字典转换为JSON格式字符串
        json_str = json.dumps(result_dict, ensure_ascii=False, indent=4)

        # 打印出JSON字符串
        print(json_str)

        # 如果你想把这个JSON字符串保存到文件
        with open(output_name, 'w', encoding='utf-8') as f:
            f.write(json_str)



if gt:
    if task=="task1":
        columns_to_convert = ['始发事件','子事件']
        filtered_df = df[columns_to_convert]
        # 构建一个字典用于保存结果
        result = {}

            # 遍历按第一列分组
#             for key, group in df.groupby("始发事件"):
# 13        # 将子事件列中的内容按格式拼接
# 14        sub_events = group["子事件"].tolist()
# 15        formatted_sub_events = "\n  ".join([f"{i+1}. {event}" for i, event in enumerate(sub_events)])
# 16        
# 17        # 添加到结果字典
# 18        result[str(key)] = {
# 19            "子事件": formatted_sub_events
# 20        }

        for key, group in filtered_df.groupby("始发事件"):
            # 构建子事件字符串
            sub_events = [f"{i+1}. {event}" for i, event in enumerate(group["子事件"].tolist())]
            event_string = "\n  ".join([f"{i+1}. {event}" for i, event in enumerate(sub_events)])
            c=1
            # 保存到结果字典中
            result[str(c)] = {
                "子事件":event_string
            }
            c=c+1
            
        output_name="input/gt_"+task+"_"+time_stamp+".json"

        # 将结果保存为json文件
        with open(output_name, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print("JSON 文件已保存。")

    elif task == "task2":
        columns_to_convert = ['操作员动作']

        # 初始化结果字典
        result_dict = {}

        # 遍历DataFrame，转换为指定的json格式
        for index, row in df.iterrows():
            result_dict[str(index + 1)] = {
                f"{col}": row[col] if pd.notnull(row[col]) else '' for col in columns_to_convert
            }

        # 将字典转换为JSON格式字符串
        json_str = json.dumps(result_dict, ensure_ascii=False, indent=4)

        # 打印出JSON字符串
        print(json_str)
        output_name="input/gt_"+task+"_"+time_stamp+".json"
        # 如果你想把这个JSON字符串保存到文件
        with open(output_name, 'w', encoding='utf-8') as f:
            f.write(json_str)

        pass
    elif task =="task3":
        columns_to_convert = ['事件树题头事件']

        # 初始化结果字典
        result_dict = {}

        # 遍历DataFrame，转换为指定的json格式
        for index, row in df.iterrows():
            result_dict[str(index + 1)] = {
                f"{col}": row[col] if pd.notnull(row[col]) else '' for col in columns_to_convert
            }

        # 将字典转换为JSON格式字符串
        json_str = json.dumps(result_dict, ensure_ascii=False, indent=4)

        # 打印出JSON字符串
        print(json_str)
        output_name="input/gt_"+task+"_"+time_stamp+".json"
        # 如果你想把这个JSON字符串保存到文件
        with open(output_name, 'w', encoding='utf-8') as f:
            f.write(json_str)

