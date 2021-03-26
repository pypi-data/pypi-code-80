def get_command_line_arguments(
    *,
    operations,
    parallel,
    projects,
    target,
    configurations,
):
    arguments = []
    arguments += [
        '--parallel', parallel,
    ]
    arguments += [
        '--target', target,
    ]
    for operation in operations:
        arguments += [
            '--operation', operation,
        ]
    for project in projects:
        arguments += [
            '--project', project,
        ]
    for configuration in configurations:
        arguments += [
            '--configuration', configuration,
        ]
    return arguments
