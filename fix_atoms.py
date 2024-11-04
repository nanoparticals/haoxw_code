import os
from pymatgen.core.structure import Structure

def fix_atoms_in_poscar(poscar_path, z_threshold=5.0):
    """
    读取 POSCAR 文件，固定 z 坐标小于 z_threshold 的原子。
    """
    # 读取 POSCAR 文件
    structure = Structure.from_file(poscar_path)

    # 遍历每个原子，设置 selective_dynamics 属性
    for site in structure.sites:
        if site.coords[2] < z_threshold:  # z 坐标小于阈值
            site.properties["selective_dynamics"] = [False, False, False]  # 固定原子
        else:
            site.properties["selective_dynamics"] = [True, True, True]  # 原子可以移动

    # 写入新的 POSCAR 文件，覆盖原文件或另存为新文件
    structure.to(filename=poscar_path, fmt="poscar", selective_dynamics=True)

def traverse_and_fix(root_dir, z_threshold=5.0):
    """
    遍历根目录下的所有子目录和文件，找到 POSCAR 文件并固定原子。
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'POSCAR':
                poscar_path = os.path.join(dirpath, filename)
                print(f"正在处理文件：{poscar_path}")
                fix_atoms_in_poscar(poscar_path, z_threshold)

if __name__ == "__main__":
    # 设置根目录为您的工作目录
    root_directory = '/home/haoxw/MEOwork/Calculate_dir/selected_cif_file_clean'

    # 设置 z 坐标阈值
    z_coord_threshold = 6.0

    # 开始处理
    traverse_and_fix(root_directory, z_coord_threshold)

