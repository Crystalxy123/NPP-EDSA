import os
import json
import matplotlib.pyplot as plt

# # # 设定你的文件夹路径
folder_path = "result/test_output_gt/task1/noReasonN"
output_path = "result/pic/test_output_gt/task1/noReasonN.png"
save_folder = "result/pic/test_output_gt/task1"

# folder_path = "result/test_output_gt/task2_modifed_all/reason_TiTou_reasonN"
# output_path = "result/pic/test_output_gt/task2_all/reason_TiTou_reasonN.png"
# save_folder = "result/pic/test_output_gt/task2"

# folder_path = "result/test_output_gt/task3/reasonN"
# output_path = "result/pic/test_output_gt/task3/reasonN.png"
# save_folder = "result/pic/test_output_gt/task3"

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 初始化两个列表以存储横坐标和纵坐标
x_data = []
y_data = []

# 获取和排序所有文件名
file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.json')], 
                    key=lambda x: int(x.split('__')[-1].split('.')[0]))

# 遍历文件夹中的所有文件
for file_name in file_names:
    # 提取文件名中的数字
    number = int(file_name.split('__')[-1].split('.')[0])
    
    # 打开并读取JSON文件
    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 统计总案例数和正确案例数
    total_cases = 0
    correct_cases = 0
    for case_data in data.values():
        if "正确案例" in case_data:
            correct_cases += 1
        total_cases += 1
    
    # 计算正确案例占比
    if total_cases > 0:
        proportion = correct_cases / total_cases
    else:
        proportion = 0
    
    # 添加数据到列表中
    x_data.append(number)
    y_data.append(proportion)

# 绘制图表
plt.figure(figsize=(10, 6))
plt.plot(x_data, y_data, marker='o', color='b')
plt.xlabel("training samples")
plt.ylabel("accuracy")

# # 添加数据标注
# for x, y in zip(x_data, y_data):
#     plt.text(x, y, f'{y:.2f}', fontsize=9, ha='right')

# 保存图像
plt.savefig(output_path, dpi=400)
# plt.show()
