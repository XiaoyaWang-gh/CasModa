from CUTE_components.models import Prefix_datapoint

STOP_DELIMETER = "END_OF_DEMO"


def embed_demo_template_updated(data: Prefix_datapoint) -> str:
    return f"""
### CLASS_NAME
{data.classname}

### CLASS_CONSTRUCTOR
{data.constructor}

### METHOD_UNDER_TEST
{data.focalname_paralist}

### TEST_METHOD_NAME
{data.testname}

### generate test input
{data.test_input}

{STOP_DELIMETER}
"""

def embed_demo_template_vanilla(data: Prefix_datapoint) -> str:
    return f"""
### CLASS_CONSTRUCTOR
{data.constructor}

### METHOD_UNDER_TEST
{data.focalname_paralist}

### TEST_METHOD_NAME
{data.testname}

### generate test input
{data.test_input}

{STOP_DELIMETER}
"""

def embed_query_template_updated(data: Prefix_datapoint) -> str:
    return f"""
### CLASS_NAME
{data.classname}

### CLASS_CONSTRUCTOR
{data.constructor}

### METHOD_UNDER_TEST
{data.focalname_paralist}

### TEST_METHOD_NAME
{data.testname}

### generate test input
"""


def embed_query_template_vanilla(data: Prefix_datapoint) -> str:
    return f"""
### CLASS_CONSTRUCTOR
{data.constructor}

### METHOD_UNDER_TEST
{data.focalname_paralist}

### TEST_METHOD_NAME
{data.testname}

### generate test input
"""
