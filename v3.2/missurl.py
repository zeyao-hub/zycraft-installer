import os


def update_file_with_prefix(file_path, prefix):
    # 检查文件是否存在且不为空
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 添加前缀到每行内容前面
        updated_lines = [prefix + line.strip() for line in lines]

        # 将更新后的内容写回文件
        with open(file_path, 'w') as file:
            file.write('\n'.join(updated_lines))
        print("文件已更新。")
    else:
        print("文件不存在或为空，无需更新。")


# 指定文件路径和前缀
file_path = 'update/updatelist/local_missing.txt'
prefix = 'https://mcmods2333.flyqilai.top/mods/'

# 调用函数进行更新
update_file_with_prefix(file_path, prefix)
