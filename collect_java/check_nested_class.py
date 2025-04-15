import re

def _remove_java_comments(code):
    # 删除所有多行注释
    code_without_multiline_comments = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # 删除所有单行注释
    code_without_any_comments = re.sub(r'//.*', '', code_without_multiline_comments)
    return code_without_any_comments

def has_nested_class(java_file_content):
    """
    Check if the given Java file content contains nested classes.
    Returns True if nested classes are found, along with the names of the outer class.
    """
    content_wo_comments = _remove_java_comments(java_file_content)
    # This regex looks for class declarations and captures the class name.
    # It's a simplified approach and might not handle all Java syntax correctly.
    class_pattern = re.compile(r'\bclass\s+([^\s{]+)')
    matches = class_pattern.findall(content_wo_comments)
    if len(matches) > 1:
        return True, matches[0]  # Assuming the first class is the outer class
    return False, None

def main():
    file_with_paths = r"C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\collect_java\core\java_file_paths.txt"  # The file containing paths to the Java files
    mark = "\\langchain4j\\"
    idx = 1
    with open(file_with_paths, 'r', encoding='utf-8') as paths_file:
        for path in paths_file:
            path = path.strip()  # Remove any leading/trailing whitespace
            try:
                with open(path, 'r', encoding='utf-8') as java_file:
                    content = java_file.read()
                    has_nested, outer_class_name = has_nested_class(content)
                    if has_nested:
                        print(f"{idx} {path[path.find(mark)+len(mark):]}")
                        idx += 1
            except FileNotFoundError:
                print(f"File not found: {path}")
            except Exception as e:
                print(f"Error processing file {path}: {e}")

if __name__ == "__main__":
    main()
