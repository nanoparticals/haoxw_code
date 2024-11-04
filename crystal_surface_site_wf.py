from pymatgen.core import Structure, Lattice, Molecule
from pymatgen.analysis.adsorption import *
from pymatgen.core.surface import generate_all_slabs
from pymatgen.core.surface import SlabGenerator,Slab
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from matplotlib import pyplot as plt
import numpy as np
import copy
import re
from pymatgen.io.xyz import XYZ
import os
import warnings
from pymatgen.io.vasp import Poscar

# 忽略 bulk_wyckoff 属性缺失的警告
warnings.filterwarnings("ignore", message="Not all sites have property bulk_wyckoff")
# 定义函数和类
class Mol_rotate_trans:
    def __init__(self, stru=None):
        self.mol = stru
        self.mols = []

    def get_rot_mols(self, ax='z', theta=[45]):
        if ax == 'x':
            ax = np.array([1, 0, 0])
        elif ax == 'y':
            ax = np.array([0, 1, 0])
        elif ax == 'z':
            ax = np.array([0, 0, 1])
        else:
            print('Wrong axis used, should be one of x, y or z')
            return []

        for t in theta:
            self.mol_temp = copy.deepcopy(self.mol)
            self.mol_temp.rotate_sites(indices=list(range(self.mol.num_sites)), theta=t, axis=ax, anchor=self.mol.center_of_mass)
            self.mols.append(copy.deepcopy(self.mol_temp))
        return self.mols

    def get_trans_mols(self, mg=None):
        final_mols = []
        for i in mg:
            self.mol_temp = copy.deepcopy(self.mol)
            n, m = i
            self.mol_temp.translate_sites(indices=list(range(self.mol_temp.num_sites)), vector=np.array([n, m, 0]))
            final_mols.append(copy.deepcopy(self.mol_temp))
        return final_mols
def similar_mols(eles=None, coord1=None, coord2=None):
    n = 0
    splited_coord1 = []
    splited_coord2 = []
    result = []
    for i in eles:
        splited_coord1.append(coord1[n:i+n])
        splited_coord2.append(coord2[n:i+n])
        n = i
    for n, cl in enumerate(splited_coord1):
        c2 = splited_coord2[n]
        if len(cl) == [(np.linalg.norm(x-y)<0.01).all() for x in cl for y in c2].count(True):
            result.append(True)
        else:
            result.append(False)
    if result.count(True) == len(cl):
        return True
    else:
        return False
def uniq_mols(mols=None):
    final_mols = []
    mols_cart_coords = [m.cart_coords for m in mols]
    eles = [int(x) for x in re.findall(r"\d", mols[0].composition.formula)]
    while len(mols) > 0:
        m0 = mols.pop(0)
        mols = [i for i in mols if not similar_mols(eles=eles, coord1=m0.cart_coords, coord2=i.cart_coords)]
        final_mols.append(m0)
    return final_mols
def similar_mols(eles=None,coord1=None,coord2=None):
    n=0
    m=0
    splited_coord1=[]
    splited_coord2=[]
    result=[]
    for i in eles: 
        splited_coord1.append(coord1[n:i+n])
        splited_coord2.append(coord2[n:i+n])
        n=i
    for n,cl in enumerate(splited_coord1):
        c2 = splited_coord2[n]
        if len(cl) == [(np.linalg.norm(x-y)<0.01).all() for x in cl for y in c2].count(True):
            result.append(True)
        else:
            result.append(False)
    if result.count(True) == len(cl):
        return(True)
    else:
        return(False)
def uniq_mols(mols=None):
    final_mols = []
    mols_cart_coords=[m.cart_coords for m in mols]
    eles = [int(x) for x in re.findall(r"\d",mols[0].composition.formula)]
    while len(mols)>0:
        m0=mols.pop(0)
        mols=[i for i in mols if not similar_mols(eles=eles,coord1=m0.cart_coords,coord2=i.cart_coords)]
        final_mols.append(m0)
    return(final_mols)    
class Add_vacuum:
   def __init__(self, stru=None):
        self.stru = stru

   def add_vac(self, axis='c', vac=18):
        coor = self.stru.cart_coords
        lattice = self.stru.lattice.parameters
        a, b, c, alpha, beta, gamma = lattice
        if axis == 'a':
            a += vac
        elif axis == 'b':
            b += vac
        elif axis == 'c':
            c += vac
        else:
            print('Wrong axis used, should be one of a, b, or c')
        temp_lattice = self.stru.lattice.from_parameters(a, b, c, alpha, beta, gamma)
        self.stru = Structure(temp_lattice, self.stru.species, coor, coords_are_cartesian=True)
        return self.stru
# 遍历文件夹中的所有 CIF 文件和 XYZ 文件
cif_dir = '/home/haoxw/MEOwork/Calculate_dir/selected_cif_files/'  # 替换为CIF文件所在目录
xyz_dir = '/home/haoxw/MEOwork/test'  # 替换为XYZ文件所在目录
cif_files = [f for f in os.listdir(cif_dir) if f.endswith('.cif')]
xyz_files = [f for f in os.listdir(xyz_dir) if f.endswith('.xyz')]
np.set_printoptions(precision=2)
for cif_file in cif_files:
    stru = Structure.from_file(os.path.join(cif_dir, cif_file))
    base_name = os.path.splitext(cif_file)[0]
    main_dir = os.path.join("/home/haoxw/MEOwork/Calculate_dir/selected_cif_files/", base_name)
    os.makedirs(main_dir, exist_ok=True)

    # 生成晶面
    s110 = SlabGenerator(stru, [1, 1, 0], min_slab_size=10, min_vacuum_size=18)
    slabs_110 = s110.get_slabs()
    s = slabs_110[1]
    s=s.get_orthogonal_c_slab()
    
    #print(len(s))

    # 保存无吸附结构
    clean_slab_path = os.path.join(main_dir, "clean", "POSCAR")
    os.makedirs(os.path.dirname(clean_slab_path), exist_ok=True)
    Poscar(s).write_file(clean_slab_path)

    for xyz_file in xyz_files:
        mol = Molecule.from_file(os.path.join(xyz_dir, xyz_file))
        adsorbate_name = os.path.splitext(xyz_file)[0]
        ads_slab_dir = os.path.join(main_dir, f"{adsorbate_name}_adsorption")
        os.makedirs(ads_slab_dir, exist_ok=True)

        # 使用 AdsorbateSiteFinder 生成吸附结构
        asf = AdsorbateSiteFinder(s, height=1.4)
       
        ads_structs = asf.generate_adsorption_structures(mol, repeat=[1, 1, 1], find_args={'positions': ['ontop']})
        filtered_ads_structs = []
        for ads_struct in ads_structs:
            # 获取距离矩阵
            dist_matrix = ads_struct.distance_matrix
            # 找到所有氧原子的索引
            oxygen_indices = [i for i, site in enumerate(ads_struct) if site.specie.symbol == 'O' and i < 96]
            print(oxygen_indices)
            
            # 获取第97号原子与所有氧原子之间的距离
            distances_to_oxygen = dist_matrix[96, oxygen_indices]
            print(distances_to_oxygen)
            # 检查第97号原子的最近氧原子距离
            if not any(dist < 2.01 for dist in distances_to_oxygen):
                 filtered_ads_structs.append(ads_struct)
                

        
        
        for i, ads_slab in enumerate(filtered_ads_structs):
            slab_path = os.path.join(ads_slab_dir, f"POSCAR_{i}.vasp")
            Poscar(ads_slab).write_file(slab_path)
           
print('ok')
import os
import shutil

def organize_poscars(base_dir):
    # 遍历所有文件和文件夹
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            # 检查文件是否是POSCAR文件
            if file.startswith("POSCAR") and file.endswith(".vasp"):
                # 获取文件的完整路径
                full_file_path = os.path.join(root, file)
                # 创建新的文件夹路径
                new_dir_path = os.path.join(root, file[:-5])  # 去掉".vasp"后缀
                # 创建文件夹
                os.makedirs(new_dir_path, exist_ok=True)
                # 定义新的文件路径
                new_file_path = os.path.join(new_dir_path, "POSCAR")
                # 移动并重命名文件
                shutil.move(full_file_path, new_file_path)

# 替换下面的路径为你的`test`文件夹的路径
base_directory = "/home/haoxw/MEOwork/Calculate_dir/selected_cif_files/"
organize_poscars(base_directory)
print('ok')
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
                    "ISMEAR": 0,  # 使用 Gamma 点方法
                    "SIGMA": 0.1,
                    "IBRION": 2,
                    "ALGO": 'Fast',
                    "LASPH":'.TRUE.',
                    "IVDW": 12,
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

