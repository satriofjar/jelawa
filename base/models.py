from django.db import models
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field

from .validators import validate_file_size


# Create your models here.
class Island(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()

    def __str__(self):
        return str(self.name)


class City(models.Model):
    island = models.ForeignKey(Island, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    video = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    text = CKEditor5Field("Question")
    img = models.ImageField(blank=True, null=True, validators=[validate_file_size])

    @property
    def imageURL(self):
        try :
            url = self.img.url
        except:
            url = ''
        return url
    
    def get_answers(self):
        return self.answer_set.all()

    def __str__(self):
        return strip_tags(self.text)[:50]


class Answer(models.Model):
    text = models.CharField("Answare", max_length=225)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
