from django.db import models


class Instance(models.Model):
    name = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=100)
    number_of_instaces = models.IntegerField()
    start_test_at = models.DateTimeField()
    command = models.CharField(max_length=100)
    instances = models.ManyToManyField(Instance)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

