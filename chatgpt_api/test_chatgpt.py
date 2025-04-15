from codex_api import CodexAPI

prefix_instruction = "Your task now is only to construct the test inputs, not the test assertions. Use CLASS_CONSTRUCTOR to get CLASS_NAME, then call TEST_METHOD_NAME. Use java without comments. End your reply with END_OF_DEMO. \n"
prefix_prompt = f"""
### CLASS_NAME
Fraction

### CLASS_CONSTRUCTOR
getReducedFraction(int numerator, int denominator)

### METHOD_UNDER_TEST
public static Fraction getReducedFraction(int numerator, int denominator)

### TEST_METHOD_NAME
testGetReducedFraction_2int()

### generate test input
int numerator = 11;
int denominator = 12;
Fraction fraction = Fraction.getReducedFraction(numerator,denominator);
END_OF_DEMO

### CLASS_NAME
Fraction

### CLASS_CONSTRUCTOR
getReducedFraction(int numerator, int denominator)

### METHOD_UNDER_TEST
public static Fraction getReducedFraction(int numerator, int denominator)

### TEST_METHOD_NAME
testGetReducedFraction_2int()

### generate test input
int numerator = 1;
int denominator = 2;
Fraction fraction = Fraction.getReducedFraction(numerator,denominator);
END_OF_DEMO

### CLASS_NAME
Fraction

### CLASS_CONSTRUCTOR
public static Fraction getReducedFraction(int numerator, int denominator)

### METHOD_UNDER_TEST
getReducedFraction(int numerator, int denominator)

### TEST_METHOD_NAME
testGetReducedFraction_2int()

### generate test input

"""


oracle_instruction = "Your task now is to generate a test assertion to replace the <OraclePlaceHolder> in UNIT_TEST. Only variables that occur after the last UNIT_TEST can be used. Use java without comments. End your reply with END_OF_DEMO.\n"
oracle_prompt = """
### METHOD_UNDER_TEST
getReducedFraction(int numerator, int denominator)

### UNIT_TEST
public void testGetReducedFraction_2int_6(){
    int numerator = 11;
    int denominator = 12;
    Fraction fraction = Fraction.getReducedFraction(numerator,denominator);

    "<OraclePlaceHolder>";
}

### generate oracle
assertTrue(fraction instanceof  Fraction);
END_OF_DEMO

### METHOD_UNDER_TEST
getReducedFraction(int numerator, int denominator)

### UNIT_TEST
public void testGetReducedFraction_2int_6(){
    int numerator = 1;
    int denominator = 2;
    Fraction fraction = Fraction.getReducedFraction(numerator,denominator);

    "<OraclePlaceHolder>";
}

### generate oracle
assertTrue(fraction instanceof  Fraction);
END_OF_DEMO

### METHOD_UNDER_TEST
getReducedFraction(int numerator, int denominator)

### UNIT_TEST
public void testGetReducedFraction_2int_6(){
    int numerator = 4;
    int denominator = 8;
    Fraction fraction = Fraction.getReducedFraction(numerator,denominator);

    "<OraclePlaceHolder>";
}

### generate oracle

"""


def main():
    model = CodexAPI("chatgpt_api/1210_test.txt")
    # prompt = prefix_instruction + prefix_prompt
    prompt = oracle_instruction + oracle_prompt
    model.get_suggestions(prompt)
    print("Done")


if __name__ == '__main__':
    main()
