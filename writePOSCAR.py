import os
from ase.io import read, write
from ase.build import sort

# 指定你想要遍历的目录路径
specified_dir = '/home/haoxw/MEOwork/Calculate_dir/selected_cif_file_clean'

# 遍历指定目录下的所有子文件夹
for root, dirs, files in os.walk(specified_dir):
    # 检查当前文件夹中是否有POSCAR文件
    if 'POSCAR' in files:
        poscar_path = os.path.join(root, 'POSCAR')
        
        # 读取POSCAR文件
        atoms = read(poscar_path)
        
        # 对原子进行排序
        atoms_sorted = sort(atoms)
        
        # 覆写POSCAR文件
        write(poscar_path, atoms_sorted)
        
        # 打印处理信息
        print(f'Processed and sorted {poscar_path}')

