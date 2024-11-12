import os
import glob

def delete_wavecar_chgcar(root_dir):
    # 遍历 root_dir 及其子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 构建 WAVECAR 和 CHGCAR 文件的完整路径
        wavecar_path = os.path.join(dirpath, 'WAVECAR')
        chgcar_path = os.path.join(dirpath, 'CHGCAR')

        # 检查并删除 WAVECAR
        if os.path.exists(wavecar_path):
            try:
                os.remove(wavecar_path)
                print(f"Deleted: {wavecar_path}")
            except Exception as e:
                print(f"Error deleting {wavecar_path}: {e}")

        # 检查并删除 CHGCAR
        if os.path.exists(chgcar_path):
            try:
                os.remove(chgcar_path)
                print(f"Deleted: {chgcar_path}")
            except Exception as e:
                print(f"Error deleting {chgcar_path}: {e}")

if __name__ == "__main__":
    # 指定需要遍历的根目录
    root_directory = "/home/haoxw/Aimcmd/work_Pt_OH/step3_gcga_3A/poscar_files"  # 修改为你要遍历的目录
    delete_wavecar_chgcar(root_directory)

