from pathlib import Path

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from ckeditor.fields import RichTextField

from problemset.utils import input_directory_path, output_directory_path, submission_directory_path
from problemset.managers import ProblemManager
from contest.models import Contest
from core.models import AbstractBaseModel

User = get_user_model()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Language(models.Model):
    name = models.CharField(verbose_name=_('Language'), max_length=200)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['-id']

    def __str__(self):
        return self.name


class Problem(AbstractBaseModel):
    class MemoryLimit(models.IntegerChoices):
        MB_64 = 64, _('64 MB')
        MB_128 = 128, _('128 MB')
        MB_256 = 256, _('256 MB')
        MB_512 = 512, _('512 MB')

    class TimeLimit(models.IntegerChoices):
        S_1 = 1, _('1 s')
        S_2 = 2, _('2 s')
        S_3 = 3, _('3 s')
        S_4 = 4, _('4 s')

    name = models.CharField(verbose_name=_('Name'), max_length=100)
    statement = RichTextField(verbose_name=_('Statement'))
    input_section = RichTextField(verbose_name=_('Input Section'))
    output_section = RichTextField(verbose_name=_('Output Section'))
    editorial = RichTextField(verbose_name=_('Editorial'))
    solution = models.FileField(verbose_name=_('Solution'))
    solution_language = models.ForeignKey(verbose_name=_('Language'), to=Language, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    is_protected = models.BooleanField(verbose_name=_('Is Protected'), default=0)
    time_limit = models.PositiveIntegerField(verbose_name=_('Time Limit'), choices=TimeLimit.choices, default=1)
    memory_limit = models.PositiveIntegerField(verbose_name=_('Memory Limit'), choices=MemoryLimit.choices, default=256)

    objects = ProblemManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Problem')
        verbose_name_plural = _('Problems')
        ordering = ['-id']


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

    class Meta:
        verbose_name = _('TestCase')
        verbose_name_plural = _('TestCases')
        ordering = ['id']

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


class Submission(AbstractBaseModel):
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
    """
    Submission Details format:
    {
        "final_verdict": "WA",
        "average_time_usage: 42, # ms
        "average_memory_usage": 432 # kb
        "results": [
            {
                testcase: 1,
                verdict: "AC",
                memory_usage: 40, # kb
                time_usage: 42 # ms
            },
            {
                testcase: 2,
                verdict: "WA",
                memory_usage: 40, # kb
                time_usage: 42 # ms
            },
            {
                testcase: 3,
                verdict: "Skipped,
                memory_usage: 0, # kb
                time_usage: 0 # ms
            }
        ]
    }
    """
    submission_details = models.JSONField(
        verbose_name=_('Submission Details'),
        default=dict,
        blank=True
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

    class Meta:
        verbose_name = _('Submission')
        verbose_name_plural = _('Submissions')
        ordering = ['-id']

    @property
    def solution_text(self):
        try:
            with open(f"{BASE_DIR}{self.solution.url}", 'r', encoding='UTF-8') as f:
                return f"\n{f.read()}"
        except FileNotFoundError:
            return 'Not Available'


class Clarification(AbstractBaseModel):
    question = models.TextField(verbose_name=_('Question'), default='')
    answer = models.TextField(verbose_name=_('Answer'), default='', blank=True)

    user = models.ForeignKey(
        verbose_name=_('User'),
        to=User,
        related_name='clarifications',
        on_delete=models.CASCADE
    )
    contest = models.ForeignKey(
        verbose_name=_('Contest'),
        to=Contest,
        related_name='clarifications',
        on_delete=models.CASCADE
    )
    problem = models.ForeignKey(
        to=Problem,
        verbose_name=_('Problem'),
        on_delete=models.CASCADE,
        related_name='clarifications'
    )

    class Meta:
        verbose_name = _('Clarification')
        verbose_name_plural = _('Clarifications')
        ordering = ['-id']
