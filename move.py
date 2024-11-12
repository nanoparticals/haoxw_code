from pymatgen.core import Structure

# 从文件或其他方式加载结构
structure = Structure.from_file("substrate.vasp")

# 计算所需的平移向量
# 这里假设你想将所有原子沿z轴平移0.5个晶胞长度
translation_vector = [0.0, 0.0, -0.1]

# 平移所有原子
structure.translate_sites(range(len(structure)), translation_vector, frac_coords=True)

# 保存平移后的结构
structure.to(fmt="POSCAR", filename="substrate.vasp")

