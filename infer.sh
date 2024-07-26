python infer.py \
    --task 3 \
    --input_path "./input/task3/data_task3_2024-05-30_test.json" \
    --model_name "gpt-4o-0513" \
    --embedding_model "text-embedding-ada-002" \
    --gt_path "./input/task3/gt_task3_2024-05-30_test.json" \
    --template_path "./templates/task1_0_shot.txt"\
    --input_eb "./result/EB/task3_gpt-4o-0513_2024-06-12-reason.json" \
    --input_nrl "./result/NRL/task3_gpt-4o-0513_2024-06-12-reason.json" \
    --output_file "./result/test_output/task3/reasonY/gpt-4o-0513_lbry4o-reason-promptReasonY"\
    --reason "Y"\
    --max "Y" \
    --check “N”\
    --beg 1

# #!/bin/bash

# # 脚本参数
# TASK=$1
# INPUT_PATH=$2
# MODEL_NAME=$3
# EMBEDDING_MODEL=$4
# GT_PATH=$5
# OUTPUT_EB=$6
# OUTPUT_NRL=$7

# # 运行 Python 脚本
# python infer.py \
#     --task $TASK \
#     --input_path $INPUT_PATH \
#     --model_name $MODEL_NAME \
#     --embedding_model $EMBEDDING_MODEL \
#     --gt_path $GT_PATH \
#     --output_eb $OUTPUT_EB \
#     --output_nrl $OUTPUT_NRL
