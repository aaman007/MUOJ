from pathlib import Path
import subprocess

from problemset.models import Submission


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Execute submitted file
def compile_submission(submission):
    # language = submission.solution_language
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
                subprocess.run(
                    f'{BASE_DIR}/media/c++/todo_coder < {input_url} > {BASE_DIR}/media/c++/todo_coder_output.txt',
                    shell=True
                )

                with open(f"{BASE_DIR}/media/c++/todo_coder_output.txt", 'r', encoding='UTF-8') as f:
                    participant_output = f.read()
                    if participant_output != testcase.output_text:
                        result = 'WA'
                        break
            except (FileNotFoundError, Exception):
                result = 'CE'
                break

    # Update submission status
    Submission.objects.filter(id=submission.id).update(status=result)
