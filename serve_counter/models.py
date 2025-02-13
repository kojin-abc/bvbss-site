from django.db import models
from django.utils.timezone import now

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length = 10)
    grade = models.IntegerField(default = 1)

    def __str__(self):
        return 'Player:id=' + str(self.id) + ', ' + self.name + '(' + str(self.grade) + ')'
    
    class Meta:
        ordering = ('id',)
    
class Game(models.Model):
    date = models.DateField(default=now)
    datestr = models.CharField(max_length=13)
    end = models.BooleanField(default = False)
    opponent = models.CharField(max_length=10)
    players = models.CharField(max_length=999) #p1,g1/p2,g2/...
    serves = models.CharField(max_length=999) #0,0,0,0,0,0/...
    results = models.CharField(max_length=999) #0,0/00,00/...
        
    def __str__(self):
        return 'Game:id=' + str(self.id) + "," + str(self.date) + " - " + self.opponent
    
    class Meta:
        ordering = ('date',)
    
    