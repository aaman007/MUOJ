from django.db import models


# Create your models here.

class language(models.Model):
    name = models.CharField(max_length=50)


class Problem(models.Model):
    name = models.CharField(max_length=100)
    statement = models.TextField()
    input_section = models.TextField()
    output_section = models.TextField()
    editorial = models.TextField()
    solution = models.FileField()
    solution_language = models.ForeignKey(to='language', on_delete=models.CASCADE)
