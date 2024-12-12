import os
import shutil

def delete_mods_directory(mods_directory_path):
    if os.path.exists(mods_directory_path):
        # 删除整个mods目录及其所有内容
        shutil.rmtree(mods_directory_path)
        print(f"目录 {mods_directory_path} 及其所有内容已删除。")
    else:
        print(f"目录 {mods_directory_path} 不存在。")

# 指定mods目录路径
mods_directory = 'mods'

# 执行删除操作
delete_mods_directory(mods_directory)
