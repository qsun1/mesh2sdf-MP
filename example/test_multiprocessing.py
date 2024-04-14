import multiprocessing
from os.path import join
from os import listdir
from test import mesh2sdf_core
import random

data_dir = './OBJ_MODELS'
NUM_cpu = 128 #5 
sdf_size = 256
dir_path = f"sdf/bnet_sdf_{sdf_size}"

def process_file(file_path):
    # 这里是处理文件的逻辑
    mesh2sdf_core(filename=file_path, save_dir=dir_path, size=sdf_size)

def main():
    # 假设有一个文件列表
    file_paths = [join(data_dir, file) for file in listdir(data_dir) if file.endswith('.obj')]
    random.shuffle(file_paths)
    print(len(file_paths))

    # 创建一个进程池，池的大小为CPU核心数，这里假设是128核
    pool = multiprocessing.Pool(processes=NUM_cpu)

    # 将文件列表中的每个文件分配给池中的进程
    pool.map(process_file, file_paths)

    # 关闭池并等待所有进程完成
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
