from pymatgen.core import Structure, Lattice, Molecule, Element
from pymatgen.analysis.adsorption import *
from pymatgen.core.surface import generate_all_slabs
from pymatgen.core.surface import SlabGenerator, Slab
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import numpy as np
import copy
import re
from pymatgen.io.xyz import XYZ
import os
import shutil  # 用于删除文件夹
import warnings
from pymatgen.io.vasp import Poscar

# 忽略 bulk_wyckoff 属性缺失的警告
warnings.filterwarnings("ignore", message="Not all sites have property bulk_wyckoff")

# 定义参数
cif_dir = '/home/haoxw/MEOwork/Calculate_dir/selected_cif_file'  # 替换为 CIF 文件所在目录
oh_xyz_path = "/home/haoxw/MEOwork/test/ohCONTCAR.xyz"  # 替换为 OH 基团的 XYZ 文件路径

# 遍历 CIF 文件
cif_files = [f for f in os.listdir(cif_dir) if f.endswith('.cif')]
np.set_printoptions(precision=2)

# 循环处理每个 CIF 文件
for cif_file in cif_files:
    # 读取结构
    stru = Structure.from_file(os.path.join(cif_dir, cif_file))
    base_name = os.path.splitext(cif_file)[0]
    main_dir = os.path.join(cif_dir, base_name)
    os.makedirs(main_dir, exist_ok=True)

    # 生成晶面（以 [1, 1, 0] 面为例，可根据需要修改）
    slab_generator = SlabGenerator(stru, [1, 1, 0], min_slab_size=10, min_vacuum_size=18)
    slabs = slab_generator.get_slabs()
    # 检查是否生成了 slab
    if not slabs:
        print(f"晶体文件 {cif_file} 无法生成指定晶面，跳过。")
        continue
    slab = slabs[1]  # 选择第一个 slab，或根据需要选择
    slab = slab.get_orthogonal_c_slab()
# 保存无吸附结构
    clean_slab_path = os.path.join(main_dir, "clean", "POSCAR")
    os.makedirs(os.path.dirname(clean_slab_path), exist_ok=True)
    Poscar(slab).write_file(clean_slab_path)


    ##### 以下为第二段代码的整合 #####

    # 读取刚才保存的无吸附结构
    structure = Structure.from_file(clean_slab_path)

    # 获取金属元素列表
    metal_elements = [el for el in structure.symbol_set if Element(el).is_metal]
    print(f"金属元素：{metal_elements}")

    # 定义一些参数
    mo_bond_length = 2.0   # 金属-氧键长，单位 Å，可根据具体金属调整
    oxygen_search_radius = 3.0  # 搜索氧原子的半径，单位 Å

    # 读取 OH 基团结构
    oh_molecule = Molecule.from_file(oh_xyz_path)

    # 获取 OH 基团的矢量方向（假设 OH 基团的原子顺序为 O、H）
    oh_o_atom = oh_molecule[0]
    oh_h_atom = oh_molecule[1]
    oh_vector = oh_h_atom.coords - oh_o_atom.coords  # OH 基团的矢量方向

    # 获取所有金属原子的索引和坐标
    metal_indices = [i for i, site in enumerate(structure)
                     if site.species_string in metal_elements]

    # 找到 z 坐标的最大值（用于识别表面原子）
    z_coords = [structure[i].coords[2] for i in metal_indices]
    max_z = max(z_coords)

    # 定义一个阈值，识别表面金属原子
    delta_z = 1.5  # 可根据需要调整
    surface_metal_indices = [i for i in metal_indices
                             if structure[i].coords[2] >= max_z - delta_z]

    print(f"表面金属原子索引：{surface_metal_indices}")

    # 检查原始结构是否具有 selective_dynamics 属性
    if 'selective_dynamics' in structure.site_properties:
        # 获取原始的 selective_dynamics 列表
        original_sd = structure.site_properties['selective_dynamics']
    else:
        # 如果没有 selective_dynamics 属性，则初始化一个默认的列表
        original_sd = [[True, True, True] for _ in structure.sites]

    # 记录已经处理的金属原子，防止重复添加 OH 基团
    processed_indices = []

    # 记录每个金属原子添加的 O 和 H 原子的索引
    metal_to_oh_indices = {}  # key: metal_index, value: [o_index, h_index]

    # 遍历每个表面金属原子，添加 OH 基团
    for metal_index in surface_metal_indices:
        if metal_index in processed_indices:
            continue  # 跳过已经处理的原子

        metal_site = structure[metal_index]
        x_m, y_m, z_m = metal_site.coords

        # 检查金属原子正上方是否已有原子（距离小于某个阈值，且 z 坐标更大）
        site_occupied = False
        for site in structure:
            x_s, y_s, z_s = site.coords
            # 判断 x 和 y 坐标接近，且 z 坐标高于金属原子，且距离小于设定值
            if (np.isclose(x_s, x_m, atol=0.1) and
                np.isclose(y_s, y_m, atol=0.1) and
                z_s > z_m and
                np.linalg.norm(site.coords - metal_site.coords) < mo_bond_length):
                site_occupied = True
                print(f"金属原子 {metal_index} 正上方已有原子，跳过。")
                break
        if site_occupied:
            continue  # 跳过被占据的位点

        # 检查正上方是否有氧原子
        has_oxygen_above = False
        for i, site in enumerate(structure):
            if site.species_string == 'O':
                x_o, y_o, z_o = site.coords
                distance = np.linalg.norm([x_o - x_m, y_o - y_m, z_o - z_m])
                if (np.isclose(x_o, x_m, atol=0.1) and
                    np.isclose(y_o, y_m, atol=0.1) and
                    z_o > z_m and
                    distance <= oxygen_search_radius):
                    has_oxygen_above = True
                    print(f"金属原子 {metal_index} 上方存在氧原子（索引 {i}），跳过。")
                    break
        if has_oxygen_above:
            continue  # 跳过不被视为活性位的金属原子
 # 新增条件：检查是否存在 y 坐标相同，且 z 坐标比金属原子大 1.3 Å 以内的原子
        has_atom_above_in_y = False
        for site in structure:
            if site == metal_site:
                continue  # 跳过自身
            y_s, z_s = site.coords[1], site.coords[2]
            if (np.isclose(y_s, y_m, atol=0.1) and
                z_s > z_m and (z_s - z_m) <= 1.3):
                has_atom_above_in_y = True
                print(f"金属原子 {metal_index} 上方存在 y 坐标相同且 z 坐标高 {z_s - z_m:.2f} Å 的原子，跳过。")
                break
        if has_atom_above_in_y:
            continue  # 跳过不满足条件的金属原子

        # 在金属原子正上方放置 OH 基团
        # 计算氧原子的位置（沿 z 轴方向，距离为金属-氧键长）
        vector_mo = np.array([0, 0, 1]) * mo_bond_length  # 假设沿 z 轴正方向
        o_position = metal_site.coords + vector_mo

        # 计算氢原子的位置（相对于氧原子的坐标，加上 OH 基团的矢量）
        h_position = o_position + oh_vector

        # 指定新添加原子的 selective_dynamics 属性
        sd_flags = [True, True, True]
        properties = {'selective_dynamics': sd_flags}

        # 添加氧原子，并记录其索引
        structure.append('O', o_position, coords_are_cartesian=True,
                         properties=properties)
        o_index = len(structure) - 1

        # 添加氢原子，并记录其索引
        structure.append('H', h_position, coords_are_cartesian=True,
                         properties=properties)
        h_index = len(structure) - 1

        # 更新 selective_dynamics 属性
        original_sd.append(sd_flags)
        original_sd.append(sd_flags)

        # 将 O 和 H 原子的索引与金属原子关联
        metal_to_oh_indices[metal_index] = [o_index, h_index]

        # 记录处理过的金属原子索引
        processed_indices.append(metal_index)

        print(f"已在金属原子 {metal_index} 处添加 OH 基团，"
              f"O 原子索引 {o_index}，H 原子索引 {h_index}。")

    # 更新结构的 site_properties
    structure.add_site_property('selective_dynamics', original_sd)


    # 对每个活性位点，移除对应的 OH 基团，并保存结构
    for idx, active_metal_index in enumerate(processed_indices):
        # 创建结构的深拷贝，避免修改原始结构
        structure_copy = copy.deepcopy(structure)
        sd_copy = copy.deepcopy(original_sd)

        # 获取对应的 O 和 H 原子索引
        oh_indices_to_remove = metal_to_oh_indices[active_metal_index]

        # 按照索引从大到小排序，确保删除原子时索引不会变化
        oh_indices_to_remove.sort(reverse=True)

        # 移除对应的 O 和 H 原子
        for index in oh_indices_to_remove:
            structure_copy.remove_sites([index])
            del sd_copy[index]

        # 更新结构的 site_properties
        structure_copy.add_site_property('selective_dynamics', sd_copy)

        # 保存修改后的结构，创建单独的文件夹
        folder_name = os.path.join(main_dir, f"site_{idx+1}")
        os.makedirs(folder_name, exist_ok=True)
        poscar_filename = os.path.join(folder_name, "POSCAR")
        structure_copy.to(fmt="poscar", filename=poscar_filename)
        print(f"已移除金属原子 {active_metal_index} 上的 OH 基团，"
              f"生成结构文件 {poscar_filename}")
 # 移除 clean 文件���
    clean_dir = os.path.join(main_dir, "clean")
    if os.path.exists(clean_dir):
        shutil.rmtree(clean_dir)
        print(f"已移除 {clean_dir} 文件夹。")
    else:
        print(f"{clean_dir} 文件夹不存在。")

    print(f"文件 {cif_file} 的所有活性位点结构已生成。")

print("所有 CIF 文件的处理已完成。")

