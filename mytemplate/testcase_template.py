from CUTE_components.models import Testcase_datapoint

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
