from pathlib import Path


def main():
    current_path = Path.cwd()
    source_dir = current_path / "ignore_it" / "1"
    target_dir = current_path / "ignore_it" / "2"
    my_generator = source_dir.glob("*.txt")

    for txt_file in my_generator:
        # 移动到target_dir
        java_file = txt_file.with_suffix(".java")
        new_java_file = target_dir / java_file.name
        new_java_file.touch()
        # 刚刚得到的.java全是空的，现在需要把.txt的内容写进去
        with open(txt_file, "r") as f:
            txt_content = f.read()
        with open(new_java_file, "w") as f:
            f.write(txt_content)


if __name__ == "__main__":
    main()
