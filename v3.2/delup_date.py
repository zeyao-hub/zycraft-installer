import os

def delete_files():
    try:
        # 读取 remote_missing.txt 文件
        with open('update/updatelist/remote_missing.txt', 'r') as file:
            files_to_delete = file.readlines()

        # 清除换行符和空白字符
        files_to_delete = [file.strip() for file in files_to_delete]

        # 从 mods 目录删除指定的文件
        mods_directory = 'modszip'
        for file_name in files_to_delete:
            file_path = os.path.join(mods_directory, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'{file_name} 已删除.')
            else:
                print(f'{file_name} 不存在于 {mods} 目录中.')

    except FileNotFoundError:
        print('找不到 remote_missing.txt 文件.')
    except Exception as e:
        print(f'发生错误: {e}')

# 调用函数执行文件删除操作
delete_files()
