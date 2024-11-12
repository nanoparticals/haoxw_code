import os
from pymatgen.core import Structure
from pymatgen.io.vasp import Poscar

def convert_contcar_to_cif(source_dir, target_dir):
    """
    将source_dir目录下所有子目录中的CONTCAR文件转换为CIF文件，并将CIF文件保存到target_dir中。
    
    :param source_dir: 包含各个计算目录的根目录
    :param target_dir: 保存CIF文件的目录
    """
    # 如果目标目录不存在，创建它
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历source_dir中的所有子目录
    for root, dirs, files in os.walk(source_dir):
        for dir_name in dirs:
            contcar_path = os.path.join(root, dir_name, 'CONTCAR')
            if os.path.exists(contcar_path):
                try:
                    # 读取CONTCAR文件
                    structure = Poscar.from_file(contcar_path).structure
                    # 生成CIF文件路径
                    cif_file_path = os.path.join(target_dir, f"{dir_name}.cif")
                    # 将结构保存为CIF文件
                    structure.to(fmt="cif", filename=cif_file_path)
                    print(f"成功将 {contcar_path} 转换为 {cif_file_path}")
                except Exception as e:
                    print(f"处理 {contcar_path} 时出错: {e}")

if __name__ == "__main__":
    # 设置源目录和目标目录
    source_directory = "./"  # 当前目录
    target_directory = "./cif_files"  # 存放CIF文件的目录

    # 执行转换
    convert_contcar_to_cif(source_directory, target_directory)

