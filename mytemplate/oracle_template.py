from CUTE_components.models import Oracle_datapoint

STOP_DELIMETER = "END_OF_DEMO"


def embed_demo_template(data: Oracle_datapoint) -> str:

    return f"""
### METHOD_UNDER_TEST
{data.focalname_paralist}

### UNIT_TEST
{data.test_method}

### generate oracle
{data.oracle}

{STOP_DELIMETER}
"""

# 和上一个方法唯一的区别就是没有最后两个占位符


def embed_query_template(data: Oracle_datapoint) -> str:
    return f"""
### METHOD_UNDER_TEST
{data.focalname_paralist}

### UNIT_TEST
{data.test_method}

### generate oracle
"""
