import os
import random
import shutil

def delete_random_folders(base_directory, percentage=10):
    # 获取所有子文件夹的列表
    all_folders = [f for f in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, f))]
    total_folders = len(all_folders)
    
    # 计算需要删除的文件夹数量
    num_to_delete = int(total_folders * (percentage / 100.0))
    
    # 随机选择要删除的文件夹
    folders_to_delete = random.sample(all_folders, num_to_delete)
    
    # 删除选定的文件夹
    for folder in folders_to_delete:
        folder_path = os.path.join(base_directory, folder)
        shutil.rmtree(folder_path)
        print(f"Deleted folder: {folder_path}")
    
    # 统计剩余文件夹数量
    remaining_folders = [f for f in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, f))]
    remaining_count = len(remaining_folders)
    
    print(f"Remaining folders: {remaining_count}")

# 设置目标目录
base_directory = '/home/haoxw/Aimcmd/live_work_Pt/H_cov/step3/perturb'  # 替换为你的目标目录路径

# 执行删除操作
delete_random_folders(base_directory, percentage=10)

