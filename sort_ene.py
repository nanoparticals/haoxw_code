import re

def extract_energy_info(log_file):
    # 用于存储结构编号和能量的列表
    energy_info = []

    # 正则表达式匹配模式
    pattern = re.compile(r'(s\d+)\s+IS BORN with G = ([\d\.]+) eV')

    # 打开文件并逐行读取
    with open(log_file, 'r') as file:
        for line in file:
            # 尝试匹配每一行
            match = pattern.search(line)
            if match:
                # 提取结构编号和能量
                structure_id = match.group(1)
                energy = float(match.group(2))
                # 将提取的信息添加到列表中
                energy_info.append((structure_id, energy))

    return energy_info

def sort_by_energy(energy_info):
    # 根据能量对列表进行排序
    return sorted(energy_info, key=lambda x: x[1])

def main():
    log_file = 'ga.log'  # 指定日志文件的路径
    energy_info = extract_energy_info(log_file)
    sorted_energy_info = sort_by_energy(energy_info)

    # 输出排序后的结果
    print("Sorted Structures by Energy:")
    for structure_id, energy in sorted_energy_info:
        print(f"{structure_id}: {energy} eV")

if __name__ == "__main__":
    main()

