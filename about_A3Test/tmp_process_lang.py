source_file = "C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/lang/focal_method.java"
target_file = "C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/lang/focal_method1.java"

CONSTRUCTOR = "WordUtils();"

# read file
with open(source_file, 'r') as f:
    lines = f.readlines()
    cnt = 0
    for i in range(2726, 2738):
        line = lines[i]
        if line.startswith("$$"):
            index = line.find(CONSTRUCTOR)
            if index != -1:
                line = line[:index]+"\n"
                cnt += 1
        with open(target_file, 'a') as tf:
            tf.write(line)

print("{}共截断了{}行".format(CONSTRUCTOR, cnt))
