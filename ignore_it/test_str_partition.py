from pathlib import Path

file_to_read = Path(
    "txt_repo/validation/lang/test_class_plus_content/BooleanUtilsTest.txt")

str_to_find = f"""@Test\n    <TestMethodPlaceHolder>"""

str_to_insert = "✨✨✨"

example = "1, public void testNegate() { Boolean bool = true; Boolean result = BooleanUtils.negate(bool); assertNotSame(bool, result); }"


def main():
    method_id, test_method = example.split(",", maxsplit=1)
    print(method_id)
    print(test_method)
    # with open(file_to_read, 'r') as f:
    #     text = f.read()
    # insert_index = text.find(str_to_find)
    # new_text = text[:insert_index] + \
    #     str_to_insert+"\n    " + text[insert_index:]
    # print(f"text:\n{text}")
    # print(f"new_text:\n{new_text}")


if __name__ == "__main__":
    main()
