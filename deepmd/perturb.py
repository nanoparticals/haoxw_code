import os
from ase.io import read, write
import numpy as np

def perturb_structure(atoms, max_displacement=0.5):
    """对原子结构进行微扰"""
    # 对每个原子的坐标施加一个随机的小扰动
    perturbation = np.random.uniform(-max_displacement, max_displacement, atoms.positions.shape)
    atoms.positions += perturbation
    return atoms

def process_directory(input_dir, output_dir, max_displacement=0.5):
    """处理输入目录中的所有结构文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file == 'CONTCAR':
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                
                atoms = read(input_path, format='vasp')
                perturbed_atoms = perturb_structure(atoms, max_displacement)
                
                output_path = os.path.join(output_subdir, 'POSCAR')
                write(output_path, perturbed_atoms, format='vasp')
                print(f"Processed {input_path} -> {output_path}")

# 定义输入和输出目录
input_directory = '/home/haoxw/Aimcmd/live_work_Pt/H_cov/step3/poscar_files'  # 替换为你的输入目录路径
output_directory = '/home/haoxw/Aimcmd/live_work_Pt/H_cov/step3/perturb'  # 替换为你的输出目录路径

# 执行微扰处理
process_directory(input_directory, output_directory, max_displacement=0.5)
