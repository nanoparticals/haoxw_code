#!/bin/bash

# 脚本名称：generate_potcar.sh
# 功能：遍历当前目录下的所有子目录，生成 POTCAR 文件

# 获取当前目录路径
current_dir=$(pwd)

# 遍历当前目录下的所有子目录
for dir in $(find "$current_dir" -type d); do
    # 跳过当前目录
    if [ "$dir" == "$current_dir" ]; then
        continue
    fi
    
    # 检查目录中是否存在 POSCAR 文件
    if [ -f "$dir/POSCAR" ] || [ -f "$dir/poscar" ]; then
        echo "正在处理目录：$dir"
        
        # 进入子目录
        cd "$dir"
        
        # 运行 VASPKIT 的任务 103 生成 POTCAR
        vaspkit -task 103
        
        # 返回上级目录
        cd "$current_dir"
    else
        echo "目录 $dir 中未找到 POSCAR 文件，跳过。"
    fi
done

echo "所有目录处理完毕！"

