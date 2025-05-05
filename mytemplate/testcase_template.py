from CUTE_components.models import Testcase_datapoint, Ecommerce_query_jsonpoint

STOP_DELIMETER = "END_OF_DEMO"


def embed_demo_template(data: Testcase_datapoint) -> str:
    return f"""
### CLASS_NAME
{data.classname}

### METHOD_UNDER_TEST
{data.focalname_paralist}
    
### TEST_METHOD_NAME
{data.test_name}

### generate test case
{data.test_body}
{STOP_DELIMETER}
"""


# 和上一个方法唯一的区别就是没有最后两个占位符
def embed_query_template(data: Testcase_datapoint) -> str:
    return f"""
### CLASS_NAME
{data.classname}

### METHOD_UNDER_TEST
{data.focalname_paralist}
    
### TEST_METHOD_NAME
{data.test_name}

### generate test case
"""


def embed_ecommerce_demo_template(data: Testcase_datapoint) -> str:
    return f"""
    
### METHOD_UNDER_TEST
{data.focal_func}

### TEST_METHOD
{data.test_body}

{STOP_DELIMETER}
"""

def embed_ecommerce_query_template(data: Ecommerce_query_jsonpoint) -> str:
    if data.rich_json != "":
        return f"""
### METHOD_UNDER_TEST
{data.rich_json}
"""
    else:
        return f"""
### METHOD_UNDER_TEST
{data.simple_json}
"""