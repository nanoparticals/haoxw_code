import math
import os
'''准备频率计算结果文件
反应物频率计算：
使用VASP对反应物进行频率计算。
将计算得到的OUTCAR文件重命名为OUTCAR_reactant。
过渡态频率计算：
使用VASP对过渡态进行频率计算。
确保过渡态只有一个虚频（负频率），对应于反应坐标。
将计算得到的OUTCAR文件重命名为OUTCAR_transition。'''
# 常量定义
h = 6.62607015e-34        # 普朗克常数，单位：J·s
k_B = 1.380649e-23        # 玻尔兹曼常数，单位：J/K
T = 298.15                # 温度，单位：K
c = 29979245800           # 光速，单位：cm/s
NA = 6.02214076e23        # 阿伏伽德罗常数，单位：1/mol

def read_frequencies(filename):
    """
    从OUTCAR文件中读取振动频率，返回频率列表，单位为Hz
    """
    frequencies = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if 'THz' in lines[i] and 'f' in lines[i]:
                line = lines[i].split()
                freq = float(line[7])
                # 将频率从THz转换为Hz
                freq_Hz = freq * 1e12
                frequencies.append(freq_Hz)
    return frequencies

def calculate_q_vib(frequencies):
    """
    计算震动配分函数 q_vib
    """
    beta = 1 / (k_B * T)
    q_vib = 1.0
    for freq in frequencies:
        # 计算每个模式的震动配分函数贡献
        x = h * freq / (k_B * T)
        q_vib *= math.exp(-x / 2) / (1 - math.exp(-x))
    return q_vib

def calculate_prefactor(q_vib_reactant, q_vib_transition):
    """
    计算指前因子 A
    """
    A = (k_B * T / h) * (q_vib_transition / q_vib_reactant)
    return A

def main():
    # 提取反应物的频率并计算q_vib
    print("读取反应物的频率...")
    frequencies_reactant = read_frequencies('OUTCAR_reactant')
    q_vib_reactant = calculate_q_vib(frequencies_reactant)
    print(f"反应物的震动配分函数 q_vib = {q_vib_reactant:e}")

    # 提取过渡态的频率并计算q_vib
    print("读取过渡态的频率...")
    frequencies_transition = read_frequencies('OUTCAR_transition')
    # 过渡态有一个虚频，需将其排除或处理
    frequencies_transition_real = [freq for freq in frequencies_transition if freq > 0]
    q_vib_transition = calculate_q_vib(frequencies_transition_real)
    print(f"过渡态的震动配分函数 q_vib = {q_vib_transition:e}")

    # 计算指前因子 A
    A = calculate_prefactor(q_vib_reactant, q_vib_transition)
    print(f"指前因子 A = {A:e} s^-1")

if __name__ == "__main__":
    main()

