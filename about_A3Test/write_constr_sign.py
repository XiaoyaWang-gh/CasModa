'''
本文件用于写query_set下的构造签名
'''

vlis7_path_prefix = "/data2/chaoni/xiaoyawang/CodeX/"

pro = "gson"

SOURCE_FILE = f"txt_repo/prefix/query_set/{pro}/classname.txt"
TARGET_FILE = f"txt_repo/prefix/query_set/{pro}/constr_sign.txt"

constr_sign_dict = {
    "ConstructorConstructor": "public ConstructorConstructor(Map<Type, InstanceCreator<?>> instanceCreators, boolean useJdkUnsafe, List<ReflectionAccessFilter> reflectionFilters)",
    "DefaultDateTypeAdapter":"DateType.DATE.createDefaultsAdapterFactory()",
    "ISO8601Utils":"ISO8601Utils",
    "JsonAdapterAnnotationTypeAdapterFactory":"public JsonAdapterAnnotationTypeAdapterFactory(ConstructorConstructor constructorConstructor)",
    "JsonReader":"public JsonReader(Reader in)",
    "JsonTreeReader":"public JsonTreeReader(JsonObject jsonObject)",
    "JsonTreeWriter":"public JsonTreeWriter()",
    "JsonWriter":"public JsonWriter(Writer out)",
    "ReflectiveTypeAdapterFactory":"ReflectiveTypeAdapterFactory(ConstructorConstructor constructorConstructor, FieldNamingStrategy fieldNamingPolicy, Excluder excluder, JsonAdapterAnnotationTypeAdapterFactory jsonAdapterFactory, List<ReflectionAccessFilter> reflectionFilters)",
    "TypeAdapters":"手动",
    "TypeInfoFactory":"TypeInfoFactory",
    "Types":"$Gson$Types",
    "UnsafeAllocator":"UnsafeAllocator.INSTANCE"
}


def main():
    with open(vlis7_path_prefix+SOURCE_FILE, "r") as cn_file:
        for line in cn_file:
            cn = line.strip()
            with open(vlis7_path_prefix+TARGET_FILE, "a") as cs_file:
                if cn.startswith("---"):
                        cs_file.write("--"*100)
                        cs_file.write("\n")
                else:
                        cs_file.write(constr_sign_dict[cn])
                        cs_file.write("\n")


if __name__ == "__main__":
    main()
