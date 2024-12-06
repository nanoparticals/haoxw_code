import os
import subprocess

def submit_vasp_jobs(root_dir):
    """
    在root_dir目录下的所有子文件夹中执行 'qsub vasp.sh' 命令。
    
    :param root_dir: 包含子文件夹的根目录
    """
    # 遍历根目录下的所有子目录
    for root, dirs, files in os.walk(root_dir):
        # 检查当前目录下是否有vasp.sh文件
        if "vasp.sh" in files:
            # 进入子目录并执行 qsub vasp.sh
            try:
                print(f"正在提交作业: {root}/vasp.sh")
                subprocess.run(["qsub", "vasp.sh"], cwd=root, check=True)
                print(f"成功提交作业: {root}/vasp.sh")
            except subprocess.CalledProcessError as e:
                print(f"提交作业失败: {root}/vasp.sh，错误信息: {e}")
            except Exception as e:
                print(f"其他错误: {e}")

if __name__ == "__main__":
    # 设置要遍历的根目录
    root_directory = "./"  # 当前目录，或根据需要修改

    # 执行作业提交
    submit_vasp_jobs(root_directory)

