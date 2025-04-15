from pathlib import Path


def main():
    current_path = Path.cwd()
    target_dir = current_path/"txt_repo"/"validation"/"cli" / \
        "output"/"evosuite"/"attempt-2"/"testunit_compile"

    conbine_file = current_path / "ignore_it" / \
        "OptionTest_from_37_to_46_stderr.txt"
    conbine_file.touch()

    with open(conbine_file, "a") as f:
        for i in range(37, 46+1):
            file_name = f"OptionTest{i}_stderr.txt"
            with open(target_dir/file_name, "r") as f2:
                f.write(f2.read())


if __name__ == "__main__":
    main()
