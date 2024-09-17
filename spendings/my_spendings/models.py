from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Category(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Expense(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=160)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()
    owner = models.ForeignKey('auth.User', related_name='expenses', on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.date})"
