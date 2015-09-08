from django.db import models
from django.contrib.postgres.fields import ArrayField

class Item(models.Model):
	item_id = models.PositiveIntegerField()
	name = models.CharField(max_length=50, default='')
	dates = ArrayField(models.DateField(auto_now=False, auto_now_add=False))
	prices = ArrayField(models.FloatField())
	volumes = ArrayField(models.FloatField())
	EMA_9 = ArrayField(models.FloatField())
	MACD = ArrayField(models.FloatField())
	histogram = ArrayField(models.FloatField())

	# def update(self):
	# 	