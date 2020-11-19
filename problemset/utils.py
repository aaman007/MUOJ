def input_directory_path(instance, filename):
    return f"testcases/input/{filename}_{instance.problem.id}"


def output_directory_path(instance, filename):
    return f"testcases/output/{filename}_{instance.problem.id}"


def submission_directory_path(instance, filename):
    """
    TODO: random unique path for each submitted file
    """
    return f"submissions/{filename}_{instance.id}_{instance.user.id}"
