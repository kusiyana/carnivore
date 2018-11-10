from django.db import models
from django.contrib import admin

class Pride (models.Model):
	name = models.CharField(max_length=128, unique=True)
	posx = models.IntegerField()
	posy = models.IntegerField()
	alive = models.IntegerField()
	def __unicode__(self):
		return self.name

class Lion(models.Model):
	parent = models.IntegerField(null=True) # parent's ID
	pride = models.ForeignKey(Pride, null = True) # pride's ID
	name = models.CharField(max_length=128, unique=True)
	age = models.IntegerField(default=0)
	sex = models.IntegerField(default=0)
	satiety = models.IntegerField(default=0)
	posx = models.FloatField() # current position
	posy = models.FloatField() # current position
	roving = models.IntegerField(default=0)
	alive = models.IntegerField(default=0)
	def __unicode__(self):
		return self.name   


class Trajectory(models.Model):
	lion = models.ForeignKey(Lion)
	elapsedtime = models.IntegerField(default=0)
	dt = models.IntegerField(default=0) #time step days
	parent = models.IntegerField(null=True) # parent's ID
	age = models.IntegerField(default=0)
	satiety = models.IntegerField(default=0)
	posx = models.FloatField() # position at time t
	posy = models.FloatField() # position at time t
	roving = models.IntegerField(default=0)
	alive = models.IntegerField(default=0)
	def __unicode__(self):
		return self.name   

#class Pridemovements(models.Model):
#	pride = models.ForeignKey(Pride)
#	time = models.IntegerField()



class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
