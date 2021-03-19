import math
from pathlib import Path
import subprocess

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


class JudgeX:
    def __init__(self, submission):
        self.language = submission.solution_language.name
        self.time_limit = submission.problem.time_limit
        self.memory_limit = submission.problem.memory_limit
        self.submission = submission
        self.test_cases = submission.problem.testcases
        self.solution_url = f"{BASE_DIR}{submission.solution.url}"
        self.result = 'AC'
        self.results = []
        self.executable_file_loc = f"{BASE_DIR}/media/userfiles/exec_{submission.user_id}"
        self.output_loc = f"{BASE_DIR}/media/userfiles/output_{submission.user_id}.txt"

    def get_extension(self):
        if self.language == 'C':
            return 'c'
        elif self.language == 'C++':
            return 'cpp'
        return 'py'

    def get_command_prefix(self):
        if self.language == 'C':
            return 'gcc'
        elif self.language == 'C++':
            return 'g++'
        return 'python3'

    def get_average_usage(self):
        time_usage = 0
        memory_usage = 0
        for res in self.results:
            time_usage += res.get("time_usage", 0)
            memory_usage += res.get("memory_usage", 0)
        time_usage /= max(1, len(self.results))
        memory_usage /= max(1, len(self.results))
        return math.ceil(time_usage), math.ceil(memory_usage)

    def get_submission_details(self):
        time_usage, memory_usage = self.get_average_usage()
        self.fill_results()
        return {
            "final_verdict": self.result,
            "average_time_usage": time_usage,
            "average_memory_usage": memory_usage,
            "results": self.results
        }

    def check_extension(self):
        """
        Check whether extension is matches for chosen language
        """
        filename = self.solution_url
        filename = filename[::-1]
        filename = filename[:filename.find('.')]
        filename = filename[::-1]
        return self.get_extension() == filename

    def create_executable_file(self):
        """
        Create an executable file for the solution named todo_coder
        """
        try:
            subprocess.run(
                f'{self.get_command_prefix()} -o {self.executable_file_loc} {self.solution_url}',
                check=True,
                shell=True
            )
        except (subprocess.CalledProcessError, Exception) as e:
            self.result = 'CE'
            self.add_result()

    def add_result(self, memory_usage=0, time_usage=0):
        self.results.append({
            "testcase": len(self.results) + 1,
            "verdict": self.result,
            "memory_usage": memory_usage,
            "time_usage": time_usage
        })

    def fill_results(self):
        count = self.test_cases.count() - len(self.results)
        for _ in range(count):
            self.results.append({
                "testcase": len(self.results) + 1,
                "verdict": "Skipped",
                "memory_usage": 0,
                "time_usage": 0
            })

    def update_submission(self):
        self.submission.status = self.result
        self.submission.submission_details = self.get_submission_details()
        self.submission.save(update_fields=['status', 'submission_details', 'modified_at'])

    def compile_cpp(self):
        self.create_executable_file()

        if self.result == 'AC':
            for index, testcase in enumerate(self.test_cases.all()):
                input_url = f"{BASE_DIR}{testcase.input.url}"

                try:
                    """ 
                    Running executable file for the given time limit and memory limit of the problem
                    Reads input from input_url file path and writes back output of the executable file in 
                    output_url file path
                    """
                    p = subprocess.run(
                        f'ulimit -t {self.time_limit}; '
                        f'ulimit -v {self.memory_limit * 1024}; '
                        f'{self.executable_file_loc} < {input_url} > {self.output_loc}',
                        shell=True
                    )
                    """
                    Return Code 0 means Executable file ran without any error
                    Return Code 137 means it didn't completed execution in given time
                    Return Code 139 means it took more memory than given memory
                    Return Code 255 means Run Time Error was caused by the code
                    """

                    if not p.returncode:
                        """
                        Reads output for the testcase and matches it with user's output
                        """
                        with open(self.output_loc, 'r', encoding='UTF-8') as f:
                            participant_output = f.read()
                            if participant_output != testcase.output_text:
                                self.result = 'WA'
                                break
                    elif p.returncode == 137:
                        self.result = 'TLE'
                        break
                    elif p.returncode == 139:
                        self.result = 'MLE'
                        break
                    else:
                        self.result = 'RTE'
                        break
                except (FileNotFoundError, Exception):
                    self.result = 'CE'
                    break
                self.add_result()
            if self.result != 'AC':
                self.add_result()

    def compile_python(self):
        if self.result == 'AC':
            for index, testcase in enumerate(self.test_cases.all()):
                input_url = f"{BASE_DIR}{testcase.input.url}"

                try:
                    with open(input_url, 'r') as infile, open(self.output_loc, 'w') as outfile:
                        p = subprocess.run(
                            f'ulimit -t {self.time_limit}; '
                            f'ulimit -v {self.memory_limit * 1024}; '
                            f"python3 {self.solution_url}",
                            shell=True,
                            stdin=infile,
                            stdout=outfile,
                            stderr=True
                        )

                        if not p.returncode:
                            with open(f"{self.output_loc}", 'r', encoding='UTF-8') as f:
                                participant_output = f.read()
                                if participant_output != testcase.output_text:
                                    self.result = 'WA'
                                    break

                        elif p.returncode == 137:
                            self.result = 'TLE'
                            break

                        else:
                            self.result = 'CE'
                            break

                except (FileNotFoundError, Exception) as e:
                    self.result = 'CE'
                    break
                self.add_result()

            if self.result != 'AC':
                self.add_result()

    def compile_and_update(self):
        if not self.check_extension():
            self.result = 'CE'
            self.add_result()
        elif self.language == 'C' or self.language == 'C++':
            self.compile_cpp()
        else:
            self.compile_python()
        self.update_submission()
