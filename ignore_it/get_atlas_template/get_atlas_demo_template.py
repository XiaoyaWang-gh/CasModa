def get_atlas_demo_template(data: models.atlas_datapoint, with_commands: bool) -> str:
    if with_commands:
        return f"""
### METHOD_UNDER_TEST:
{data.focal_method}
### UNIT_TEST
{data.test_method}
[METHOD_UNDER_TEST]: {data.method_name}
[UNIT_TEST]: {data.test_name}
### generate assertion
{data.assertion}
{STOP_DELIMETER}
"""
    else:
        return f"""
{data.focal_method}
{data.test_method}
### generate assertion
{data.assertion}
{STOP_DELIMETER}
        """