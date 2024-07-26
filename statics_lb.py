import argparse
import json
import pdb
import matplotlib.pyplot as plt


# 初始化一个字典来存储每个键的"正确案例"数量
correct_case_counts = {}


def count_specific_keys(data, num):
    sum=0
    for key, value in data.items():
        try:
            key_int = int(key)
            if key_int < num+1:
                correct_case_counts[key] = len(value.get("错误案例", []))
                sum = sum +correct_case_counts[key]
            else:
                pass
        except ValueError:
            # 如果键不能转换为整数，则跳过
            continue
    return sum

def generate_target_keys(n):
    return [str(i) for i in range(1, n + 1)]


def plotxy(x,y1,y2,figure_name):

    # 创建一个新的图表
    plt.figure()

    # 绘制第一个数据系列，使用红色线条和点
    plt.plot(x, y1, 'ro-', label='Experience_Base')  # 'r' 是红色，'o' 是点，'-' 是线条
    print(len(y1))

    # 绘制第二个数据系列，使用蓝色线条和点
    plt.plot(x, y2, 'bo-', label='Nuclear_Record_Library')  # 'b' 是蓝色，'o' 是点，'-' 是线条

    # 添加标签
    plt.xlabel('Training Samples')
    plt.ylabel('Generated Samples')
    if max(y1)>max(y2):
        plt.ylim(-0.5, max(y1)+4) 
    else:
        plt.ylim(-0.5, max(y2)+1) 
    
    plt.xlim(0, len(y2)+0.5) 
    plt.legend()

    # 移除网格线
    plt.grid(False)

    # 使横纵坐标轴刻度包裹数据
    plt.margins(x=0, y=0)

    
    plt.savefig(figure_name, dpi=400)
    # 显示绘制的图表
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path_eb", type=str, default="./input/output_task3_0520.json", help="测试的json文件_eb")
    parser.add_argument("--input_path_nr", type=str, default="./input/output_task3_0520.json", help="测试的json文件_nr")
    parser.add_argument("--figure_name", type=str, default="./input/output_task3_0520.json", help="生成的图像保存地址")
    
    args = parser.parse_args()

    input_path_eb = args.input_path_eb
    input_path_nr = args.input_path_nr
    figure_name = args.figure_name

    with open(input_path_eb, 'r', encoding='utf-8') as file:
        data_eb = json.load(file)
    with open(input_path_nr, 'r', encoding='utf-8') as file:
        data_nr = json.load(file)

    num = len(data_nr)
        # Example usage
    count_eb=[]
    for i in range(1,num+1):
    # Get the count of each key
        count = count_specific_keys(data_eb, i)
        # 打印结果
        count_eb.append(count)
    print(count_eb)
    # 使用 range() 和 list() 生成列表 [1, 2, 3, ..., n]
    number_list = list(range(1, num + 1))
    # pdb.set_trace()
    plotxy(number_list,count_eb,number_list,figure_name)




# 打印生成的列表
print(number_list)


