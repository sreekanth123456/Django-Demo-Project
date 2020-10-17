from django.db import models

class Form1Model(models.Model):
	unique_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
	inquirer_name = models.CharField(max_length=100, default='')
	expected_life = models.IntegerField()
	color = models.CharField(max_length=20, default='')


class Form2Model(models.Model):
	unique_id = models.CharField(max_length=100, null=True, blank=True)
	exposed_to = models.CharField(max_length=20, default='')
	vehicle= models.CharField(max_length=200, default='')
	year_built= models.CharField(max_length=200, default='')
	comments = models.TextField(blank=True, null=True)