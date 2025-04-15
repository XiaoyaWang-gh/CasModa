TARGET_FILE = "/data2/chaoni/xiaoyawang/CodeX/txt_repo/oracle/query_set/gson/fake_token_count.txt"


def main():
    with open(TARGET_FILE, "a") as f:
        for i in range(129):
            f.write("0\n")


if __name__ == "__main__":
    main()
