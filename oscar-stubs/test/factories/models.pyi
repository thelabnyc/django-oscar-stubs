from django.db import models

class Band(models.Model):
    name: models.CharField

class Member(models.Model):
    name: models.CharField
    band: models.ForeignKey[Band, Band]
