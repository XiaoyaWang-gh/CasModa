import re


def hascode(input_str):
    '''
    这个方法用于检测一个字符串(通常是chatgpt的回复)中是否包含代码
    input_str: str 输入的字符串
    result: bool
    '''
    if not input_str:  # 如果输入的字符串为空，显然不会有代码块
        return False
    has_code = re.search(r'`java\n(.*?)\n`', input_str, re.DOTALL)
    if has_code:
        return True
    else:
        return False


def delete_test_class_shell(chatgpt_out: str) -> str:
    '''  
    该方法的作用是从字符串中提取 类签名 后面的内容（不包含大括号）  
    '''
    pattern = r'\bclass\b\s+[A-Za-z_]\w*(\s*:\s*[^{]+)?'
    find_res = bool(re.search(pattern, chatgpt_out))
    if not find_res:  # 如果找不到 "public class"
        return chatgpt_out  # 说明本身就是一个test method了

    start_index = chatgpt_out.find(
        "{") + 1  # 查找第一个大括号的位置，并将索引移动到大括号后面
    end_index = chatgpt_out.rfind("}")  # 查找最后一个大括号的位置

    if end_index == -1 or end_index <= start_index:  # 如果找不到最后一个大括号或者最后一个大括号在起始位置之前
        return ""  # 返回空字符串

    return chatgpt_out[start_index:end_index]  # 返回从起始位置到最后一个大括号之前的内容


def fetch_method_chatgpt_out(chatgpt_out: str) -> str:
    '''
    该方法的作用是从chatgpt的回复中提取出方法
    chatgpt_out: str chatgpt的回复
    '''
    # 匹配代码块，匹配到则提取
    match = re.search(r'`java\n(.*?)\n`', chatgpt_out, re.DOTALL)
    if match:
        tmp_out = match.group(1)
    else:
        return ""
    # 删除所有的@Test
    tmp_out = tmp_out.replace("@Test", "")
    # 删除以import开头的代码行
    tmp_out = re.sub(r'^\s*import.*$', '', tmp_out, flags=re.MULTILINE)
    # 删除以//开头的代码行
    tmp_out = re.sub(r'^\s*//.*$', '', tmp_out, flags=re.MULTILINE)

    # 删除测试类的壳子
    tmp_out = delete_test_class_shell(tmp_out)
    # 返回结果
    return tmp_out


def form_complete_statement(chatgpt_out: str) -> str:
    '''
    该方法的作用是将chatgpt的回复中的代码片段补全
    '''
    chatgpt_out = chatgpt_out.strip('\n')  # 删除头尾的换行符
    if not chatgpt_out.endswith(';'):  # 如果不以分号结尾
        chatgpt_out += ';'  # 添加分号
    return chatgpt_out


def make_classpath(*args):
    """
    用于制作命令行进行编译或执行时候的classpath
    可以输入不定个数个路径    
    """
    classpath = ";".join(args)  # windows下的命令行用分号分隔
    classpath += " "  # 否则和后面黏在一起 javac: 无源文件

    return classpath
