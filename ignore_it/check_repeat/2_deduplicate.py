SF = "ignore_it/check_repeat/lang/class_method.txt"
TF = "ignore_it/check_repeat/lang/deduplicated_class_method.txt"


def main():
    with open(SF, "r") as sf:
        sf_list = sf.readlines()
        unique_set = set(sf_list)
        unique_list = list(unique_set)

    with open(TF, "a") as tf:
        tf.write("".join(unique_list))


if __name__ == '__main__':
    main()
