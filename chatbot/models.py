from django.db import models

# Create your models here.
class Answers(models.Model):
	answer = models.TextField(max_length=200)
	def __str__(self):
		return "%s" % self.answer

class Keywords(models.Model):
	keyword = models.TextField(max_length=100)
	answers = models.ManyToManyField('Answers')
	def __str__(self):
		return "%s" % self.keyword