from CUTE_components.models import Failed_To_Be_Repair_datapoint


def test_failed_repair_template(data: Failed_To_Be_Repair_datapoint) -> str:
    return f"""
The last test case you generated against `{data.focalname_paralist}` \
in `{data.classname}` had some test failure and stdout as follows: \
`{data.failed_stderr}`. 
The failed test case is as follows:
```{data.test_unit}```
Please generate a new test case to pass the test based on the above information. And don't give a test class, a test method is enough.
"""
