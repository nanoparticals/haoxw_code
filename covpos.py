import os
from pymatgen.core import Structure
from pymatgen.io.vasp import Poscar

def convert_cif_to_poscar(source_dir, target_dir):
    """
    将source_dir目录下的所有.cif文件转换为POSCAR文件，并将它们保存到target_dir中的对应文件夹中。
    
    :param source_dir: 包含.cif文件的目录
    :param target_dir: 保存POSCAR文件的根目录
    """
    # 如果目标目录不存在，则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历source_dir下的所有文件
    for file_name in os.listdir(source_dir):
        if file_name.endswith(".cif"):
            cif_file_path = os.path.join(source_dir, file_name)
            # 获取文件名（不带扩展名），用于命名文件夹和POSCAR文件
            folder_name = os.path.splitext(file_name)[0]
            folder_path = os.path.join(target_dir, folder_name)
            
            # 创建对应的文件夹
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            try:
                # 读取.cif文件
                structure = Structure.from_file(cif_file_path)
                # 生成POSCAR文件路径
                poscar_file_path = os.path.join(folder_path, "POSCAR")
                # 将结构保存为POSCAR文件
                poscar = Poscar(structure)
                poscar.write_file(poscar_file_path)
                print(f"成功将 {cif_file_path} 转换为 {poscar_file_path}")
            except Exception as e:
                print(f"处理 {cif_file_path} 时出错: {e}")

if __name__ == "__main__":
    # 设置源目录和目标目录
    source_directory = "./cif_files"  # 包含cif文件的目录
    target_directory = "./poscar_files"  # 保存POSCAR文件的根目录

    # 执行转换
    convert_cif_to_poscar(source_directory, target_directory)

