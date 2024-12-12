def clear_file_content(file_path):
    try:
        with open(file_path, 'w') as file:
            file.write('')
        print(f"Cleared content of {file_path}")
    except Exception as e:
        print(f"Error clearing content of {file_path}: {e}")


def main():
    files_to_clear = [
        'update/updatelist/local_missing.txt',
        'update/updatelist/remote_missing.txt'
    ]

    for file_path in files_to_clear:
        clear_file_content(file_path)


if __name__ == "__main__":
    main()
