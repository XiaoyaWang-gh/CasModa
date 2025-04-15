from util.use_unixcoder import sort_by_cossimi, cosine_similarity, encode_by_unixcoder


def main():

    # weight_list = [0.68, 0.26, 0.77, 0.80, 0.25]
    # def my_weight(x):
    #     return weight_list[x]

    # print("my expected sorted id list is [2, 1, 3, 4, 0]")
    # idx_list = [x for x in range(len(weight_list))]
    # print(f"idx_list is {idx_list}")
    # weight_list = [my_weight(x) for x in idx_list]
    # print(f"weight_list is {weight_list}")
    # sorted_idx_list = sorted(
    #     idx_list, key=my_weight, reverse=False)
    # sorted_weight_list = [my_weight(x) for x in sorted_idx_list]
    # print(f"sorted_weight_list is {sorted_weight_list}")
    # print(f"actual list is {sorted_idx_list}")

    test_query = "This is the base sentence."
    test_list = [
        "This is a similar sentence.",
        "This sentence is quite similar.",
        "Here is a sentence that resembles the base sentence.",
        "A sentence similar to the base sentence.",
        "This sentence is completely different."
    ]

    test_query_tensor = encode_by_unixcoder(test_query)
    test_list_tensor = [encode_by_unixcoder(i) for i in test_list]
    test_similarity_list = [cosine_similarity(
        test_query_tensor, i) for i in test_list_tensor]
    idx_list = sort_by_cossimi(test_query, test_list)

    print(test_similarity_list)
    print(idx_list)
    sorted_test_list = [test_list[i] for i in idx_list]
    print(sorted_test_list)


if __name__ == '__main__':
    main()
