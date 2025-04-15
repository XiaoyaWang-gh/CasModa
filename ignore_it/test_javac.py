import subprocess


def main():
    suffix = "javac -J-Duser.language=en -cp"
    class_path_list = [
        "C:\\dataset\\d4j-spec5\\2_cli\\2.0\\commons-cli2\\src\\java",
        "C:\\Libraries\\maven-3.5.0\\lib\\*"
    ]
    test_class_path = "C:\\dataset\\d4j-spec5\\2_cli\\2.0\\commons-cli2\\src\\test\\org\\apache\\commons\\cli2\\generated_by_chatgpt\\HelpFormatterTestTmp.java"
    javac_cmd = f"{suffix} {';'.join(class_path_list)} {test_class_path}"

    compile_result = subprocess.run(javac_cmd, shell=True,
                                    capture_output=True, text=True)
    print(f"compile_result.args")
    print(f"compile_result.returncode:{compile_result.returncode}")
    print(
        f"if stderr in dir(compile_result):{hasattr(compile_result, 'stderr')}")
    print(f"compile_result.stderr:{compile_result.stderr}")
    print(
        f"if stdout in dir(compile_result):{hasattr(compile_result, 'stdout')}")
    print(f"compile_result.stdout:{compile_result.stdout}")


if __name__ == "__main__":
    main()
