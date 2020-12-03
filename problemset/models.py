from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from pathlib import Path

from problemset.utils import input_directory_path, output_directory_path, submission_directory_path
from problemset.managers import ProblemManager
from contest.models import Contest

User = get_user_model()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Language(models.Model):
    name = models.CharField(verbose_name=_('Language'), max_length=200)

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.CharField(max_length=100)
    statement = models.TextField()
    input_section = models.TextField()
    output_section = models.TextField()
    editorial = models.TextField()
    solution = models.FileField(verbose_name=_('Solution'))
    solution_language = models.ForeignKey(verbose_name=_('Language'), to=Language, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    is_protected = models.BooleanField(default=0)
    time_limit = models.IntegerField(verbose_name=_('Time Limit'), default=1)
    memory_limit = models.PositiveIntegerField(verbose_name=_('Memory Limit'), default=256)

    objects = ProblemManager()

    def __str__(self):
        return self.name


class TestCase(models.Model):
    label = models.CharField(verbose_name=_('Label'), max_length=200, blank=True)
    input = models.FileField(verbose_name=_('Input File'), upload_to=input_directory_path)
    output = models.FileField(verbose_name=_('Output File'), upload_to=output_directory_path)

    is_sample = models.BooleanField(verbose_name=_('Is Sample'), default=False)
    notes = models.TextField(verbose_name=_('Notes'), blank=True)
    problem = models.ForeignKey(
        verbose_name=_('Problem'),
        to=Problem,
        related_name='testcases',
        on_delete=models.CASCADE
    )

    @property
    def input_text(self):
        try:
            with open(f"{BASE_DIR}{self.input.url}", 'r', encoding='UTF-8') as f:
                return f.read()
        except FileNotFoundError:
            return 'Not Available'

    @property
    def output_text(self):
        try:
            with open(f"{BASE_DIR}{self.output.url}", 'r', encoding='UTF-8') as f:
                return f.read()
        except FileNotFoundError:
            return 'Not Available'


class Submission(models.Model):
    STATUS_CHOICES = (
        ('Running', 'Running'),
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('TLE', 'Time Limit Exceeded'),
        ('MLE', 'Memory Limit Exceeded'),
        ('CE', 'Compilation Error')
    )

    solution = models.FileField(verbose_name=_('Solution'), upload_to=submission_directory_path)
    solution_language = models.ForeignKey(
        verbose_name=_(' Language'),
        to=Language,
        related_name='submissions',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        verbose_name=_('Status'),
        choices=STATUS_CHOICES,
        default='Running',
        max_length=200
    )

    contest = models.ForeignKey(
        verbose_name=_('Contest'),
        to=Contest,
        related_name='submissions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    problem = models.ForeignKey(
        verbose_name=_('Problem'),
        to=Problem,
        related_name='submissions',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name=_('User'),
        to=User,
        related_name='submissions',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
