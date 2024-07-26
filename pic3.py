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

def process_directory(folder_path):
    x_data = []
    y_data = []

    file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.json')], 
                        key=lambda x: int(x.split('__')[-1].split('.')[0]))

    for file_name in file_names:
        number = int(file_name.split('__')[-1].split('.')[0])
        
        with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        total_cases = 0
        correct_cases = 0
        for case_data in data.values():
            if "正确案例" in case_data:
                correct_cases += 1
            total_cases += 1
        
        if total_cases > 0:
            proportion = correct_cases / total_cases
        else:
            proportion = 0
        
        x_data.append(number)
        y_data.append(proportion)
    
    return x_data, y_data


# 创建保存目录
save_folder = "result/pic/output/"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

output_path = os.path.join(save_folder, "task1_noreasonNY.png")

# 绘制图表
plt.figure(figsize=(10, 6))

# colors = ['b', 'g', 'r','y']  # 不同目录使用不同颜色
colors = ['r','y']

for idx, (folder_path, label) in enumerate(directories):
    x_data, y_data = process_directory(folder_path)
    plt.plot(x_data, y_data, marker='o', color=colors[idx], label=label)

plt.xlabel("Training Samples")
plt.ylabel("Accuracy")
plt.legend()

# 保存图像
plt.savefig(output_path, dpi=400)
