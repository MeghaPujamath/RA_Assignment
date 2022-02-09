from django.db import models

class Matching(models.Model):
    n = models.DecimalField(decimal_places=0, max_digits=10000, default=int('1'))