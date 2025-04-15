from pygments.lexers import JavaLexer
from pygments.token import Token


def check_java_syntax(code):
    lexer = JavaLexer()
    try:
        tokens = lexer.get_tokens(code)
        for token in tokens:
            if token[0] == Token.Error:
                return False
    except Exception as e:
        return False
    return True


def main():

    java_code = """
    public class MyClass {
        public static void main(String[] args) {
            JsonReader reader = new JsonReader(reader("{\"a\": [1, 2, 3], \"b\": 4, \"c\": {\"d\": 5}}")); reader.beginObject(); reader.skipValue(); assertThat(reader.peek()).isEqualTo(JsonToken.BEGIN_OBJECT); reader.skipValue(); assertThat(reader.peek()).isEqualTo(JsonToken.END_OB
        }
    }
    """

    if check_java_syntax(java_code):
        print("The syntax is correct!")
    else:
        print("There is a syntax error in the code.")


if __name__ == "__main__":
    main()
