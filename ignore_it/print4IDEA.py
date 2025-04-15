# 包含主函数的python文件

def main():
    for i in range(10):
        try:
            if i == 5:
                raise Exception("触发异常")
            print(i)
        except Exception as e:
            print("发生异常:", e)
            continue


if __name__ == '__main__':
    main()
