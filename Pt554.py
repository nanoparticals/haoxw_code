from ase import Atoms
from ase.io import read, write
from ase.build import surface
from ase.visualize import view

# ==========================
# 步骤 1：读取 Pt 块体结构
# ==========================
try:
    # 尝试读取 Pt 块体结构文件
    bulk_pt = read('Pt.cif')
  #  bulk_pt = bulk_pt.repeat((1,1,1))
    print("成功读取 Pt 块体结构文件。")
except Exception as e:
    # 如果无法读取，打印错误信息
    print("无法读取 Pt 块体结构文件，请检查文件路径和格式。")
    print(f"错误信息：{e}")
    exit()

# ==========================
# 步骤 2：定义 (554) 晶面
# ==========================
miller_index = (5, 5, 4)

# ==========================
# 步骤 3：构建 (554) 晶面
# ==========================
layers = 10 # 原子层数，可根据需要调整
vacuum = 0    # 真空层厚度，单位为 Å

slab = surface(bulk_pt, miller_index, layers=layers, vacuum=vacuum)
#view(slab)
# 将 slab 居中并添加真空层
slab.center(axis=2, vacuum=vacuum)

# ==========================
# 步骤 4：调整晶胞尺寸（可选）
# ==========================
# 如果需要扩大表面尺寸，可以重复 slab
repeat_times = (4, 1, 1)  # 在 x, y, z 方向的重复次数
slab = slab.repeat(repeat_times)
#slab = slab*(1,4,1)
# ==========================
# 步骤 5：保存并可视化
# ==========================
# 保存为 .cif 文件
output_filename = 'Pt_554_slab.cif'
write(output_filename, slab)
print(f"已成功保存 {output_filename} 。")

# 可视化检查
view(slab)

