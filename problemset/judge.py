from pathlib import Path
import subprocess

from problemset.models import Submission


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# C++ code compile
def compile_cpp_submission(submission):
    solution_url = f"{BASE_DIR}{submission.solution.url}"
    result = 'AC'

    # Create an executable file for the solution named todo_coder
    try:
        subprocess.check_output(f'g++ -o {BASE_DIR}/media/c++/todo_coder {solution_url}', shell=True)
    except (subprocess.CalledProcessError, Exception):
        result = 'CE'

    if result == 'AC':
        for testcase in submission.problem.testcases.all():
            input_url = f"{BASE_DIR}{testcase.input.url}"

            try:
                p = subprocess.run(
                    f'ulimit -t {submission.problem.time_limit}; '
                    f'ulimit -v {submission.problem.memory_limit*1024}; '
                    f'{BASE_DIR}/media/c++/todo_coder < {input_url} > {BASE_DIR}/media/c++/todo_coder_output.txt',
                    shell=True
                )
                if not p.returncode:
                    with open(f"{BASE_DIR}/media/c++/todo_coder_output.txt", 'r', encoding='UTF-8') as f:
                        participant_output = f.read()
                        if participant_output != testcase.output_text:
                            result = 'WA'
                            break
                elif p.returncode == 137:
                    result = 'TLE'
                elif p.returncode == 139:
                    result = 'MLE'
                else:
                    result = 'RTE'
            except (FileNotFoundError, Exception):
                result = 'CE'
                break

    # Update submission status
    Submission.objects.filter(id=submission.id).update(status=result)


# Execute submitted file
def compile_submission(submission):
    language = submission.solution_language

    if language.name == 'C++':
        compile_cpp_submission(submission)
