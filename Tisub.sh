#!/bin/bash

#PBS -N test
#PBS -l nodes=1:ppn=32
#PBS -l walltime=1200:00:00
#PBS -q batch
#PBS -V
source /opt/intel/compilers_and_libraries_2018/linux/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64
source /opt/intel/impi/2018.1.163/bin64/mpivars.sh

cd $PBS_O_WORKDIR

# 定义 VASP 需要的输入文件列表
input_files=("POSCAR" "POTCAR" "INCAR" "KPOINTS")

# 定义 selected_cif_files 的根目录
root_dir="/home/haoxw/MEOwork/Calculate_dir/selected_cif_file_clean"

# 遍历 root_dir 下所有以 'Cu' 开头的目录
for cu_dir in "$root_dir"/Ti*/; do
    # 检查目录是否存在（防止无匹配的情况）
    if [ -d "$cu_dir" ]; then
        echo "正在处理目录：$cu_dir"
        
        # 在当前 'Cu' 目录下递归搜索所有子目录
        find "$cu_dir" -type d | while read dir; do
            # 初始化一个标志，用来检查所有文件是否存在
            all_files_exist=true

            # 检查每个输入文件是否存在于目录中
            for file in "${input_files[@]}"; do
                if [ ! -f "$dir/$file" ]; then
                    # 如��文件不存在，设置标志位为 false 并退出循环
                    all_files_exist=false
                    break
                fi
            done

            # 如果所有文件都存在，则提交作业
            if [ "$all_files_exist" = true ]; then
                echo "提交 VASP 作业于目录 $dir"
                cd "$dir"
                NP=$(wc -l < "$PBS_NODEFILE")
                NN=$(sort "$PBS_NODEFILE" | uniq | tee "/tmp/nodes.$$" | wc -l)
                cat "$PBS_NODEFILE" > "/tmp/nodefile.$$"
                mpirun -genv I_MPI_DEVICE ssm -machinefile "/tmp/nodefile.$$" -n "$NP" /opt/vasp.5.4.1/bin/vasp_std
                cd -  # 返回到之前的工作目录
            fi
        done
    else
        echo "目录 $cu_dir 不存在。"
    fi
done

echo "已完成所有作业。"

rm -rf "/tmp/nodefile.$$"
rm -rf "/tmp/nodes.$$"

