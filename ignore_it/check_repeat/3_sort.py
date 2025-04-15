SF = "ignore_it/check_repeat/chart/deduplicated_class_method.txt"
TF = "ignore_it/check_repeat/chart/sorted_class_method.txt"


def main():

    with open(SF, "r") as sf:
        sf_list = sf.readlines()
        sorted_list = sorted(sf_list, key=lambda x: x.split(" ", 1)[0])

    with open(TF, "a") as tf:
        tf.write("".join(sorted_list))


if __name__ == '__main__':
    main()
