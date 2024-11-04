import os
from pymatgen.io.vasp.inputs import Incar, Kpoints, Poscar, Potcar

def generate_vasp_files_for_directory(test_directory):
    for root, dirs, files in os.walk(test_directory):
        for file in files:
            if file == "POSCAR":
                poscar_path = os.path.join(root, file)
                structure = Poscar.from_file(poscar_path).structure

                # 创建自定义的 INCAR
                incar = Incar({
                    "ENCUT": 400,
                    "ISMEAR": 0, 
                    "SIGMA": 0.1,
                    "IBRION": 2,
                    "ALGO": 'Fast',
                    "LASPH":'.TRUE.',
                    "IVDW": 11,
                    "ISYM": 0,
                    "NCORE": 16,
                    "EDIFFG":-0.05,
                    "NSW":500
                })

                # 创建 Gamma 点的 KPOINTS
                kpoints = Kpoints.gamma_automatic([4, 2, 1])

                # 创建 POTCAR，假设使用 PBE 赝势
                potcar = Potcar(symbols=[site.species_string for site in structure], functional="PBE")

                # 保存文件
                incar.write_file(os.path.join(root, 'INCAR'))
                kpoints.write_file(os.path.join(root, 'KPOINTS'))
                potcar.write_file(os.path.join(root, 'POTCAR'))

                print(f"Generated VASP files for {poscar_path}")

# 指定 test 目录
test_directory = "/home/haoxw/MEOwork/Calculate_dir/selected_cif_files/"
generate_vasp_files_for_directory(test_directory)
import os
import shutil

def distribute_shell_script(script_path, root_directory):
    """
    将指定的 shell 脚本复制到包含 VASP 输入文件的每个目录中。

    :param script_path: shell 脚本的完整路径
    :param root_directory: 需要遍历的根目录
    """
    # 确保脚本文件存在
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"The script file '{script_path}' does not exist.")

    # 遍历目录
    for subdir, dirs, files in os.walk(root_directory):
        # 检查是否为 VASP 输入文件目录
        if set(['INCAR', 'KPOINTS', 'POSCAR', 'POTCAR']).issubset(set(files)):
            # 构建目标路径
            target_script_path = os.path.join(subdir, os.path.basename(script_path))
            # 复制文件
            shutil.copy(script_path, target_script_path)
            print(f"Copied '{script_path}' to '{target_script_path}'")

# 使用示例
script_path = '/home/haoxw/MEOwork/vasp-mu01.sh'
root_directory = '/home/haoxw/MEOwork/Calculate_dir/selected_cif_files/'
distribute_shell_script(script_path, root_directory)
