PATH_PREFIX = "C:\dataset\d4j-spec5\A3Test provided"

file_dict = {
    "chart": PATH_PREFIX+"\chart.txt",
    "cli": PATH_PREFIX+"\cli.txt",
    "csv": PATH_PREFIX+"\csv.txt",
    "gson": PATH_PREFIX+"\gson.txt",
    "lang": PATH_PREFIX+"\lang.txt"
}

def count_file(path):
    count = 0
    with open(path, "r") as f:
        for line in f:
            count += 1
    return count

def count_public(path):
    count = 0
    with open(path, "r") as f:
        for line in f:
            # count number of "public" in line
            count += line.count("public")
    return count

def print_first_line(path):
    with open(path, "r") as f:
        # print first line of f
        return f.readline()

def main():
    for key in file_dict:
        num_line = count_file(file_dict[key])
        num_public = count_public(file_dict[key])
        print(f"{key} num_line : {num_line}")
        print(f"{key} num_public : {num_public}")
        print(f"平均每个item含有{round(num_public/num_line,2)}个public")

if __name__ == "__main__":
    main()