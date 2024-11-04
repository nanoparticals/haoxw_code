crystal_surface_site_wf.py是MEO切晶面并生成四个输入文件并放入提交脚本的代码
input.py是生成四个输入文件并将脚本放入对应文件夹的代码
fix_atoms.py是固定Z坐标以下的的原子位置不动的的脚本
calculate_prefactor.py是用过渡态CINEB计算动力学指前因子的脚本
sqs_generate_v6_ir.ipynb是生成MEO特殊准随机结构的脚本
screen是高通量筛选提取相同名称，能量最低的结构的脚本
bulk_input_V1.ipynb是在计算bulk能量的时候，为所有cif文件生成vasp输入文件的脚本
adsorp_pymatgen_v8.ipynb是crystal_surface_site_wf.py的notebook版
move.py调整晶胞在晶格内的位置的脚本
covcif.py将所有CONTCAR转换为cif文件的脚本
covpos.py将所有cif文件转换为POSCAR的脚本
delwavchg.py删除所有文件夹中wavecar和chgcar的脚本
generate_structures.py是对活性位点之外的位点生成OH覆盖
writePOSCAR.py是覆写POSCAR让POSCAR中的元素变规整避免重复的脚本
generate_potcar.sh是用vaspkit生成POTCAR的bash脚本
Pt554.py生成554晶面的代码
Tisub.sh提交所有以Ti开头的文件占用一个节点循环提交任务
