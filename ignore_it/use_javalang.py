import javalang
import black

PLACE_HOLDER = ''' "<OraclePlaceHolder>"; '''


input = '''
    TypeAdapter<Number> numberAdapter = new TypeAdapter<Number>() {
        @Override
        public void write(JsonWriter out, Number value) throws IOException {
            out.value(value);
        }

        @Override
        public Number read(JsonReader in) throws IOException {
            return in.nextInt();
        }
    };
    TypeAdapterFactory factory = TypeAdapters.newTypeHierarchyFactory(Number.class, numberAdapter);
    TypeAdapter<Integer> integerAdapter = new TypeAdapter<Number>() {
        @Override
        public void write(JsonWriter out, Number value) throws IOException {
            out.value(value);
        }

        @Override
        public Number read(JsonReader in) throws IOException {
            return in.nextLong();
        }
    };
'''

input2 = '''
TypeInfoFactory.getTypeInfoForArray(int[].class);
TypeInfoFactory.getTypeInfoForArray(String[].class);
TypeInfoFactory.getTypeInfoForArray(int[].class);
TypeInfoFactory.getTypeInfoForArray(String[].class);
TypeInfoFactory.getTypeInfoForArray(int[].class);

'''

input3 = '''
TypeInfoFactory.getTypeInfoForArray(int[].class);
'''

input4 = '''
int a = 4; 
int b = 2.7182818;
for(int i=0;i<200;i++){
System.out.println("焦虑成这样，不应该");
}
'''

input5 = '''int a = 4; int b = 2.7182818; int c = a + b;'''

input6 = '''int a = 4; int b = 2.7182818; for(int i=0;i<200;i++){ System.out.println("焦虑成这样，不应该"); }'''

input7 = '''    
TypeAdapterFactory factory = TypeAdapters.newTypeHierarchyFactory(Number.class, numberAdapter); TypeAdapter<Integer> integerAdapter = new TypeAdapter<Number>() { @Override public void write(JsonWriter out, Number value) throws IOException { out.value(value); } @Override public Number read(JsonReader in) throws IOException { return in.nextLong(); } };
'''





def insert_oracle(java_method_body: str):

    # java_method_body = format_java_code(java_method_body)
    # print(java_method_body)
    code_added_newline = '\n'+java_method_body+'\n'

    java_class = f'''
    public class TempClass {{ 
        public void tempMethod() {{
            {code_added_newline}
        }}  
    }}
    '''

    tree = javalang.parse.parse(java_class)
    class_declaration = tree.types[0]
    method_declaration = class_declaration.methods[0]

    last_statement = method_declaration.body[-1]
    last_statement_start = last_statement._position
    last_statement_line = last_statement_start.line

    lines = java_class.splitlines()
    new_lines = lines[:last_statement_line-1] + \
        [PLACE_HOLDER] + lines[last_statement_line-1:]
    modified_code = "\n".join(new_lines)

    modified_statements = modified_code.split('\n')[3:-3]
    modified_statements_code = "\n".join(modified_statements)

    return modified_statements_code


def main():
    midware = format_java_code(input7)
    print(midware)
    endres = insert_oracle(midware)
    print(endres)


if __name__ == '__main__':
    main()
