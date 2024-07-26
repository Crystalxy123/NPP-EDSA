# -*- coding: utf-8 -*-

import argparse
import os
import base64
import json
from tqdm import tqdm
import requests
import re
import time
from multiprocessing import Pool  
import datetime  
from collections import defaultdict

from gpt_text import get_gpt_text, get_gpt_text_new
from gpt_embedding import get_embedding
import numpy as np

from tqdm import tqdm
import pdb

# 获取当前时间
import datetime
# time_stamp = datetime.datetime.now().strftime("%Y-%m-%d")
time_stamp = datetime.datetime.now().strftime("%Y-%m-%d")




def cosine_similarity(embedding1, embedding2):
    # 计算两个嵌入向量的余弦相似度
    dot_product = sum(a*b for a, b in zip(embedding1, embedding2))
    magnitude1 = sum(a*a for a in embedding1) ** 0.5
    magnitude2 = sum(a*a for a in embedding2) ** 0.5
    if magnitude1 * magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)


# 读取现有的输出JSON文件
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def append_to_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)





def extract_sub_events(text,task):
    if task =="task1":
        # 定义匹配子事件的正则表达式：数字+点号+空格+文本
        pattern = r"\d+\..*"
        
        # 找到所有匹配项
        matches = re.findall(pattern, text)
        
        # 将多个匹配项连接成一个字符串，并用换行符分隔
        sub_events = "\n".join(matches)
    elif task=="task2":
        if ": " in text:
            sub_events=text.split(": ")[1]
        else:
            sub_events = text
    elif task=="task3":
        if ": " in text:
            sub_events=text.split(": ")[1]
        else:
            sub_events = text
    
    return sub_events

def extract_dialogue(task, text):
    if task == "task2":
        pattern = r"(核电厂策略建议人员：|核电厂策略检验人员：)(.*?)(?=(核电厂策略建议人员：|核电厂策略检验人员：|$))"
    elif task == "task1":
        pattern = r"(核电厂始发事件子事件分析人员：|核电厂子事件检验人员：)(.*?)(?=(核电厂始发事件子事件分析人员：|核电厂子事件检验人员：|$))"
    elif task == "task3":
        pattern = r"(核电厂事件树题头事件分析人员：|核电厂题头事件检验人员：)(.*?)(?=(核电厂事件树题头事件分析人员：|核电厂题头事件检验人员：|$))"
    matches = re.findall(pattern, text, re.DOTALL)
    results = [(match[0].rstrip(':'), match[1].strip()) for match in matches]
    return results

def get_response(task, model_name, accident_desc, prompt_template, retrieval, cnt):
    if task == "task1":
        if retrieval == '' :
            prompt = f"####指令描述：{prompt_template}\n####请你根据以下始发事件的描述给我子事件列表：{accident_desc}\n"
        else:
            prompt = f"####指令描述：{prompt_template}\n####已知{retrieval}\n 请你根据以下始发事件的描述给我子事件列表：{accident_desc}\n"
    elif task =="task2":
        if retrieval == '' :
            prompt = f"####指令描述：{prompt_template}\n####请你根据以下内容给我操作员动作：{accident_desc}\n"
        else:
            prompt = f"####指令描述：{prompt_template}\n####已知{retrieval}\n 请你根据以下内容给我操作员动作：{accident_desc}\n"
    elif task =="task3":
        if retrieval == '' :
            prompt = f"####指令描述：{prompt_template}\n####请你根据以下内容给我事件树题头事件：{accident_desc}\n"
        else:
            prompt = f"####指令描述：{prompt_template}\n####已知{retrieval}\n 请你根据以下内容给我事件树题头事件：{accident_desc}\n"

    cnt += 1
    # pdb.set_trace()
    res = get_gpt_text_new(model_name, prompt)
    return res

def get_response_agent2(task, model_name, accident_desc,result_extract,gt_desc):
    with open(f"./templates/{task}_agent2.txt", "r", encoding='utf-8') as file:
        prompt_template_agent = file.read()
    if task == "task1":
        prompt = f"####指令描述：{prompt_template_agent}\n####{accident_desc}\n####核电厂始发事件子事件分析人员得到的始发事件子事件：{result_extract}\n \
    ####真实的子事件：{gt_desc}"
    elif task == "task2":
        prompt = f"####指令描述：{prompt_template_agent}\n####{accident_desc}\n####核电厂策略建议人员得到的操作员动作：{result_extract}\n \
        ####真实的操作员动作：{gt_desc}"
    elif task == "task3":
        prompt = f"####指令描述：{prompt_template_agent}\n####{accident_desc}\n####核电厂事件树题头事件分析人员得到的题头事件：{result_extract}\n \
        ####真实的题头事件：{gt_desc}"
    # pdb.set_trace()
    res = get_gpt_text_new(model_name, prompt)
    return res

def create_file(file_name, file_content):
   try:
       with open(file_name, 'w') as file:
           file.write(file_content)
       print(f"File '{file_name}' created successfully with the provided content.")
   except Exception as e:
       print(f"An error occurred: {e}")

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return []

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def append_to_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
       json.dump(data, file, ensure_ascii=False, indent=4)






def load_json_file(file_path):
    if os.path.getsize(file_path) == 0:
        print(f"The file '{file_path}' is empty.")
        return None
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# def get_retrieval(output_nrl,output_eb,accident_desc,idx):
#     if not (os.path.exists(output_nrl)):  
#         retrieval = ""
#         create_file(output_nrl,retrieval)
#         return retrieval
#     elif not (os.path.exists(output_eb)):
#         retrieval = ""
#         create_file(output_nrl,retrieval)
#         return retrieval
#     else:
#         nrl_data = load_json_file(output_nrl)
#         eb_data = load_json_file(output_eb)
#         if task =="task1":   
#             if nrl_data == None and eb_data == None:
#                 retrieval=''
#             elif nrl_data == None and eb_data != None:
#                 retrieval = ""
#                 for key, value in eb_data.items():
#                     error_cases_first_elements = [case_group[0] for case_group in eb_data[str(key)]['错误案例']]
#                     error_cases = "对于始发事件："+eb_data[str(key)]['始发事件']+"\n"
#                     result_error_str = ' 或 '.join(error_cases_first_elements).replace("核电厂始发事件子事件分析人员：", "")
#                     retrieval = retrieval+"##"+error_cases+"子事件并不是："+result_error_str
                
                

#             elif nrl_data != None and eb_data == None:
#                 retrieval = ""
#                 for key, value in nrl_data.items():
#                     right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(key)]['正确案例']]
#                     right_cases = "对于始发事件："+nrl_data[str(key)]['始发事件']+"\n"
#                     result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂始发事件子事件分析人员：", "")
#                     retrieval = retrieval+"##"+right_cases+"子事件是："+result_right_str
                

#             else:
#                 retrieval = ""
#                 for key, value in eb_data.items():
#                 # for key, value in student.items():
#                     error_cases_first_elements = [case_group[0] for case_group in eb_data[str(key)]['错误案例']]
#                     error_cases = "对于始发事件："+eb_data[str(key)]['始发事件']+"\n"
#                     result_error_str = ' 或 '.join(error_cases_first_elements).replace("核电厂始发事件子事件分析人员：", "")
#                     retrieval = retrieval+"##"+error_cases+"子事件并不是："+result_error_str

#                 for key, value in nrl_data.items():
#                     right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(key)]['正确案例']]
#                     right_cases = "对于始发事件："+nrl_data[str(key)]['始发事件']+"\n"
#                     result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂始发事件子事件分析人员：", "")
#                     retrieval = retrieval+"##"+right_cases+"子事件是："+result_right_str
#         elif task == "task2":
#             if nrl_data == None and eb_data == None:
#                 retrieval=''
#             elif nrl_data == None and eb_data != None:
#                 retrieval = ""
#                 for key, value in eb_data.items():
#                     error_cases_first_elements = [case_group[0] for case_group in eb_data[str(key)]['错误案例']]
#                     error_cases = "对于子事件："+eb_data[str(key)]['子事件']+"\n"
#                     result_error_str = ' 或 '.join(error_cases_first_elements).replace("核电厂策略建议人员：", "")
#                     retrieval = retrieval+"##"+error_cases+"的操作员策略建议并不是："+result_error_str
                
                

#             elif nrl_data != None and eb_data == None:
#                 retrieval = ""
#                 for key, value in nrl_data.items():
#                     right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(key)]['正确案例']]
#                     right_cases = "对于子事件："+nrl_data[str(key)]['子事件']+"\n"
#                     result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂策略建议人员：", "")
#                     retrieval = retrieval+"##"+right_cases+"的操作员策略建议是："+result_right_str
                

#             else:
#                 retrieval = ""
#                 for key, value in eb_data.items():
#                 # for key, value in student.items():
#                     error_cases_first_elements = [case_group[0] for case_group in eb_data[str(key)]['错误案例']]
#                     error_cases = "对于子事件："+eb_data[str(key)]['子事件']+"\n"
#                     result_error_str = ' 或 '.join(error_cases_first_elements).replace("核电厂策略建议人员：", "")
#                     retrieval = retrieval+"##"+error_cases+"的操作员策略建议并不是："+result_error_str

#                 for key, value in nrl_data.items():
#                     right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(key)]['正确案例']]
#                     right_cases = "对于子事件："+nrl_data[str(key)]['子事件']+"\n"
#                     result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂策略建议人员：", "")
#                     retrieval = retrieval+"##"+right_cases+"的操作员策略建议是："+result_right_str

#         return retrieval

def get_similarity(str1,str2):
    accident_embedding = get_embedding(embedding_model=embedding_model, text=str(str1))
    lib_embedding =get_embedding(embedding_model=embedding_model, text=str(str2))
    return cosine_similarity(accident_embedding,lib_embedding)

def find_best(accident_desc, data,task,TiTou):
    max_similarity = 0
    best_match_id = None
    if task =="task1":
        for key, value in data.items():
            similarity_event  = get_similarity( accident_desc.get('始发事件'),data[str(key)]["始发事件"] )
            similarity_description = get_similarity( accident_desc.get('始发事件描述'),data[str(key)]["始发事件描述"] )
            combined_similarity = (similarity_event + similarity_description) / 2  # 平均相似度
            if combined_similarity > max_similarity:
                max_similarity = combined_similarity
                best_match_id = key
        return best_match_id
    elif task=="task2":
        for key, value in data.items():
            similarity_event  = get_similarity( accident_desc.get('始发事件'),data[str(key)]["始发事件"] )
            similarity_description = get_similarity( accident_desc.get('始发事件描述'),data[str(key)]["始发事件描述"] )
            similarity_3 = get_similarity( accident_desc.get('子事件'),data[str(key)]["子事件"] )
            similarity_4 = get_similarity( accident_desc.get('事件进程和系统响应'),data[str(key)]["事件进程和系统响应"] )
            if TiTou=="Y":
                similarity_5 = get_similarity( accident_desc.get('事件树题头事件'),data[str(key)]["事件树题头事件"] )
                combined_similarity = (similarity_event + similarity_description+similarity_3+similarity_4+similarity_5) / 5  # 平均相似度
            else:
                # similarity_5 = get_similarity( accident_desc.get('事件树题头事件'),data[str(key)]["事件树题头事件"] )
                combined_similarity = (similarity_event + similarity_description+similarity_3+similarity_4) / 4  # 平均相似度

            if combined_similarity > max_similarity:
                max_similarity = combined_similarity
                best_match_id = key
        return best_match_id
    elif task=="task3":
        for key, value in data.items():
            similarity_event  = get_similarity( accident_desc.get('始发事件'),data[str(key)]["始发事件"] )
            similarity_description = get_similarity( accident_desc.get('始发事件描述'),data[str(key)]["始发事件描述"] )
            similarity_3 = get_similarity( accident_desc.get('子事件'),data[str(key)]["子事件"] )
            similarity_4 = get_similarity( accident_desc.get('事件进程和系统响应'),data[str(key)]["事件进程和系统响应"] )
            combined_similarity = (similarity_event + similarity_description+similarity_3+similarity_4) / 4  # 平均相似度
            if combined_similarity > max_similarity:
                max_similarity = combined_similarity
                best_match_id = key
        return best_match_id
    else:
        pass


def get_retrieval(output_nrl,output_eb,accident_desc,idx,reason,TiTou):
    accident_embedding = get_embedding(embedding_model=embedding_model, text=str(accident_desc)) # tokens limitation

    if not (os.path.exists(output_nrl)):  
        retrieval = ""
        create_file(output_nrl,retrieval)
        return retrieval
    elif not (os.path.exists(output_eb)):
        retrieval = ""
        create_file(output_eb,retrieval)
        return retrieval
    else:
        nrl_data = load_json_file(output_nrl)
        eb_data = load_json_file(output_eb)
        if task =="task1":   
            if nrl_data == None and eb_data == None:
                retrieval=''
            elif nrl_data == None and eb_data != None:
                retrieval = ""
                # result = [{"始发事件": eb_data[id_]["始发事件"], "始发事件描述": eb_data[id_]["始发事件描述"]} for id_ in eb_data]
            
                best_match_id = find_best(accident_desc, eb_data,task,TiTou)
                error_cases = "对于始发事件："+eb_data[str(best_match_id)]['始发事件']+"\n"
                for case_group in eb_data[str(best_match_id)]['错误案例']:
                    if reason=="Y":
                        retrieval = retrieval+"##错误案例："+error_cases+"子事件并不是："+case_group[0].split("：")[1]+",原因是：\n"+case_group[1].split("：")[1]+"\n"
                    else:
                        retrieval = retrieval+"##错误案例："+error_cases+"子事件并不是："+case_group[0].split("：")[1]
                   
                

            elif nrl_data != None and eb_data == None:
                retrieval = ""
                best_match_id = find_best(accident_desc, nrl_data,task,TiTou)
                right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(best_match_id)]['正确案例']]
                right_cases = "对于始发事件："+nrl_data[str(best_match_id)]['始发事件']+"\n"
                result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂始发事件子事件分析人员：", "")
                retrieval = retrieval+"##正确案例："+right_cases+"子事件是："+result_right_str
                

            else:
                retrieval = ""
                best_match_id_eb = find_best(accident_desc, eb_data,task,TiTou)
                error_cases = "对于始发事件："+eb_data[str(best_match_id_eb)]['始发事件']+"\n"
                for case_group in eb_data[str(best_match_id_eb)]['错误案例']:
                    if reason == "Y":
                        retrieval = retrieval+"##错误案例："+error_cases+"子事件并不是："+case_group[0].split("：")[1]+",原因是：\n"+case_group[1].split("：")[1]+"\n"
                    else:
                        retrieval = retrieval+"##错误案例："+error_cases+"子事件并不是："+case_group[0].split("：")[1]

                

                best_match_id_rl = find_best(accident_desc, nrl_data,task,TiTou)
                right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(best_match_id_rl)]['正确案例']]
                right_cases = "对于始发事件："+nrl_data[str(best_match_id_rl)]['始发事件']+"\n"
                result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂始发事件子事件分析人员：", "")
                retrieval = retrieval+"##正确案例："+right_cases+"子事件是："+result_right_str
                
        elif task == "task2":
            if nrl_data == None and eb_data == None:
                retrieval=''
            elif nrl_data == None and eb_data != None:
                retrieval = ""
                best_match_id = find_best(accident_desc, eb_data,task,TiTou)
                error_cases = "对于子事件："+eb_data[str(best_match_id)]['子事件']+"\n"
                for case_group in eb_data[str(best_match_id)]['错误案例']:
                    if reason == "Y":
                        retrieval = retrieval+"##错误案例："+error_cases+"的操作员策略建议并不是："+case_group[0].split("：")[1]+"，原因是：\n"+case_group[1].split("：")[1]+"\n"
                    else:
                        retrieval = retrieval+"##错误案例："+error_cases+"的操作员策略建议并不是："+case_group[0].split("：")[1]

                

            elif nrl_data != None and eb_data == None:
                retrieval = ""
                best_match_id = find_best(accident_desc, nrl_data,task,TiTou)
                right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(best_match_id)]['正确案例']]
                right_cases = "对于子事件："+nrl_data[str(best_match_id)]['子事件']+"\n"
                result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂策略建议人员：", "")
                retrieval = retrieval+"##正确案例："+right_cases+"的操作员策略建议是："+result_right_str
                
            else:
                retrieval = ""
                best_match_id_eb = find_best(accident_desc, eb_data,task,TiTou)
                error_cases = "对于子事件："+eb_data[str(best_match_id_eb)]['子事件']+"\n"
                for case_group in eb_data[str(best_match_id_eb)]['错误案例']:
                    if reason =="Y":
                        retrieval = retrieval+"##错误案例："+error_cases+"的操作员策略建议并不是："+case_group[0].split("：")[1]+"，原因是：\n"+case_group[1].split("：")[1]+"\n"
                    else:
                        retrieval = retrieval+"##错误案例："+error_cases+"的操作员策略建议并不是："+case_group[0].split("：")[1]


                best_match_id_rl = find_best(accident_desc, nrl_data,task,TiTou)
                right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(best_match_id_rl)]['正确案例']]
                right_cases = "对于子事件："+nrl_data[str(best_match_id_rl)]['子事件']+"\n"
                result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂策略建议人员：", "")
                retrieval = retrieval+"##正确案例："+right_cases+"的操作员策略建议是："+result_right_str
        elif task == "task3":
            if nrl_data == None and eb_data == None:
                retrieval=''
            elif nrl_data == None and eb_data != None:
                retrieval = ""
                best_match_id = find_best(accident_desc, eb_data,task,TiTou)
                error_cases = "对于子事件："+eb_data[str(best_match_id)]['子事件']+"\n"
                for case_group in eb_data[str(best_match_id)]['错误案例']:
                    if reason == "Y":
                        retrieval = retrieval+"##错误案例："+error_cases+"的事件树题头事件并不是："+case_group[0].split("：")[1]+"，原因是：\n"+case_group[1].split("：")[1]+"\n"
                    else:
                        retrieval = retrieval+"##错误案例："+error_cases+"的事件树题头事件并不是："+case_group[0].split("：")[1]

                

            elif nrl_data != None and eb_data == None:
                retrieval = ""
                best_match_id = find_best(accident_desc, nrl_data,task,TiTou)
                right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(best_match_id)]['正确案例']]
                right_cases = "对于子事件："+nrl_data[str(best_match_id)]['子事件']+"\n"
                result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂事件树题头事件分析人员：", "")
                retrieval = retrieval+"##正确案例："+right_cases+"的事件树题头事件是："+result_right_str
                
            else:
                retrieval = ""
                best_match_id_eb = find_best(accident_desc, eb_data,task,TiTou)
                error_cases = "对于子事件："+eb_data[str(best_match_id_eb)]['子事件']+"\n"
                for case_group in eb_data[str(best_match_id_eb)]['错误案例']:
                    if reason =="Y":
                        retrieval = retrieval+"##错误案例："+error_cases+"的事件树题头事件并不是："+case_group[0].split("：")[1]+"，原因是：\n"+case_group[1].split("：")[1]+"\n"
                    else:
                        retrieval = retrieval+"##错误案例："+error_cases+"的事件树题头事件并不是："+case_group[0].split("：")[1]


                best_match_id_rl = find_best(accident_desc, nrl_data,task,TiTou)
                right_cases_first_elements = [case_group[0] for case_group in nrl_data[str(best_match_id_rl)]['正确案例']]
                right_cases = "对于子事件："+nrl_data[str(best_match_id_rl)]['子事件']+"\n"
                result_right_str = ' 或 '.join(right_cases_first_elements).replace("核电厂事件树题头事件分析人员：", "")
                retrieval = retrieval+"##正确案例："+right_cases+"的事件树题头事件是："+result_right_str

        return retrieval




def process_worker(args):
    accident_desc, gt_desc, prompt_template, task, model_name, embedding_model, output_nrl, output_eb, idx,reason,max,check,TiTou = args

    circle=1
    next=0 # 是否切换到下一种案例
    while circle==1:
        # accident_embedding = get_embedding(embedding_model=embedding_model, text=str(accident_desc)) # tokens limitation
        # gt_embedding = get_embedding(embedding_model=embedding_model, text=str(gt_desc))

        retrieval = get_retrieval(output_nrl,output_eb,accident_desc,idx,reason,TiTou)
        result = get_response(task, model_name, accident_desc, prompt_template, retrieval, cnt=0)
        result_extract = extract_sub_events(result,task)
        # if result_extract 
        print(result_extract)
        # res_embedding = get_embedding(embedding_model=embedding_model, text=str(result))

        if task == "task1":
            
            nct =1
            verify_word = get_response_agent2(task, model_name, accident_desc,result_extract,gt_desc)
            # if cosine_similarity(res_embedding, gt_embedding) > 0.90:
            if '否' in verify_word or '不一致'  in verify_word or verify_word[0]=="否":
                command_word = "否"
                command_text ="错误案例"
                next = 0
                
            else:
                command_word = "是" 
                command_text ="正确案例"
                next=1
                circle =0
                
            # 初始化结果字典

            results = defaultdict(lambda: {command_text: []})
            for key, value in accident_desc.items():
                results[idx][key] = value
            results[idx][command_text].append(["核电厂始发事件子事件分析人员："+result_extract,"\n核电厂子事件检验人员："+verify_word])
          
            output_file = output_nrl if command_word == "是" else output_eb
            existing_data = read_json(output_file)
            for item_idx, item in results.items():
                found = False
                for existing_item in existing_data:
                    if str(item_idx) in existing_item:
                        found = True
                        existing_data[str(item_idx)][command_text].extend(item[command_text])
                        break
                if not found:
                    existing_data[str(item_idx)] = item
            # 更新文件
            append_to_json(output_file, existing_data)


        elif task=="task2":#识别操作员动作
            # 无否定，存入Nuclear Record Library
            nct =1
            verify_word = get_response_agent2(task, model_name, accident_desc,result_extract,gt_desc)
            # if cosine_similarity(res_embedding, gt_embedding) > 0.90:
            if '否' in verify_word:
                command_word = "否"
                command_text ="错误案例"
                next = 0
                
            else:
                command_word = "是" 
                command_text ="正确案例"
                next=1
                circle =0
            # 初始化结果字典

            results = defaultdict(lambda: {command_text: []})
            for key, value in accident_desc.items():
                results[idx][key] = value
            results[idx][command_text].append(["核电厂策略建议人员："+result_extract,"\n核电厂策略检验人员："+verify_word])

          
            output_file = output_nrl if command_word == "是" else output_eb
            existing_data = read_json(output_file)
            for item_idx, item in results.items():
                found = False
                for existing_item in existing_data:
                    if str(item_idx) in existing_item:
                        found = True
                        existing_data[str(item_idx)][command_text].extend(item[command_text])
                        break
                if not found:
                    existing_data[str(item_idx)] = item
            # 更新文件
            append_to_json(output_file, existing_data)
        elif task =="task3":
             # 无否定，存入Nuclear Record Library
            nct =1
            verify_word = get_response_agent2(task, model_name, accident_desc,result_extract,gt_desc)
            # if cosine_similarity(res_embedding, gt_embedding) > 0.90:
            if '否' in verify_word:
                command_word = "否"
                command_text ="错误案例"
                next = 0
                
            else:
                command_word = "是" 
                command_text ="正确案例"
                next=1
                circle =0
                
            # 初始化结果字典

            results = defaultdict(lambda: {command_text: []})
            for key, value in accident_desc.items():
                results[idx][key] = value
            results[idx][command_text].append(["核电厂事件树题头事件分析人员："+result_extract,"\核电厂题头事件检验人员："+verify_word])

          
            output_file = output_nrl if command_word == "是" else output_eb
            existing_data = read_json(output_file)
            for item_idx, item in results.items():
                found = False
                for existing_item in existing_data:
                    if str(item_idx) in existing_item:
                        found = True
                        existing_data[str(item_idx)][command_text].extend(item[command_text])
                        break
                if not found:
                    existing_data[str(item_idx)] = item
            # 更新文件
            append_to_json(output_file, existing_data)
    

def main(prompt_template, input_path, gt_datapath, task, model_name, embedding_model, output_nrl, output_eb,reason,max,check,TiTou):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    accident_set = list(data.values())
    idx_list = list(data.keys())
    
    with open(gt_datapath, 'r', encoding='utf-8') as file:
        gt = json.load(file)
    gt_set = list(gt.values())
    gt_idx_list =list(gt.keys())
    

    key=''
    # args_list = []
    for idx, accident_desc, gt_desc in tqdm(zip(idx_list, accident_set, gt_set), total=len(idx_list)):
        # args_list.append((accident_desc, prompt_template, task, model_name, output_nrl, output_eb, idx))
        if task == "task1":
            key = '子事件'
        elif task == "task2":
            key = "操作员动作"
        elif task =="task3":
            key = "事件树题头事件"
        args_list = (accident_desc,gt_desc[key], prompt_template, task, model_name, embedding_model, output_nrl, output_eb, idx,reason, max, check,TiTou)
        process_worker(args=args_list)

  


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=int, default=1, help="task1 识别始发事件; task2 识别操作员动作; task3 识别事件树题头")
    parser.add_argument("--input_path", type=str, default="./input/output_task3_0520.json", help="input path")
    parser.add_argument("--model_name", type=str, default="gpt-4o-0513", help="gpt-4o-0513, gpt-4-1106, gpt-4-0409, gpt-4-turbo-128k, gpt-3.5-16K-1106")
    parser.add_argument("--embedding_model", type=str, default="text-embedding-ada-002", help="text_embedding_ada_002")
    parser.add_argument("--gt_path", type=str, default="./input/gt_task1_2024-05-28.json", help="gt path")
    parser.add_argument("--reason", type=str, default="Y", help="Y/N")
    parser.add_argument("--max", type=str, default="Y", help="Y/N")
    parser.add_argument("--check", type=str, default="Y", help="Y/N")
    parser.add_argument("--TiTou", type=str, default="Y", help="Y/N")

    args = parser.parse_args()

    task = f"task{str(args.task)}"
    model_name = args.model_name
    embedding_model = args.embedding_model
    input_datapath = args.input_path
    gt_datapath = args.gt_path
    output_nrl = f"./Nuclear_Record_Library/{task}_{model_name}_{time_stamp}.json"
    output_eb = f"./Experience_Base/{task}_{model_name}_{time_stamp}.json"
    reason = args.reason
    max=args.max
    check = args.check
    TiTou = args.TiTou

    # try:
        # 分析指南：\
        # 确定关键因素：首先识别描述中提到的所有关键元素，包括设备、人员、环境条件等。\
        # 事件序列还原：根据描述，梳理事故发生的顺序和事件之间的因果关系。\
        # 识别始发事件：在事件序列中追溯，找到导致一系列后续事故发生的最初事件或条件。\
    # with open(f"./templates/task1_0_shot.txt", "r", encoding='utf-8') as file:
    with open(f"./templates/{task}.txt", "r", encoding='utf-8') as file:
        prompt_template = file.read()
    
    main(prompt_template, input_datapath, gt_datapath, task, model_name, embedding_model, output_nrl, output_eb,reason,max,check,TiTou)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     print("Restarting script...")
    #     time.sleep(1)
        


