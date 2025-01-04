import os
from ase.io import read

# 定义输入目录
input_directory = '/home/haoxw/Aimcmd/live_work_Pt/H_cov/step3/poscar_files/s001619'  # 替换为你的目录路径

# 定义 z 方向距离阈值
z_threshold = 5.0  # z 方向距离阈值为 5 Å
# 遍历目录中的所有文件
for filename in os.listdir(input_directory):
    if filename.startswith('POSCAR'):  # 仅处理POSCAR文件
        filepath = os.path.join(input_directory, filename)
        
        # 尝试读取POSCAR文件
        try:
            # 使用 ASE 读取POSCAR文件
            atoms = read(filepath, format='vasp')
            
            # 提取原子位置
            positions = atoms.get_positions()
            
            # 找到 z 方向距离小于 5 Å 的原子，并将它们的索引加一
            modified_indices = []
            for i, pos in enumerate(positions):
                z_distance = pos[2]  # 获取 z 坐标
                if z_distance < z_threshold:
                    modified_indices.append(i + 1)  # 索引加一
                    print(f"Atom index: {i}, Z-distance: {z_distance:.2f} Å")
            
            # 输出结果
            if modified_indices:
                output = ' '.join(map(str, modified_indices))
                print(f"File: {filename}, Modified Atom Indices: {output}")
            else:
                print(f"File: {filename}, No atoms found with z < {z_threshold} Å")
        
        except Exception as e:
            print(f"Failed to read file {filename}: {e}")
