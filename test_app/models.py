from django.db import models

# Create your models here.


class Compani(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Cars(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=25)
    number = models.IntegerField()
    compani = models.ForeignKey(
        Compani, related_name="Compani", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PetModel(models.Model):
    kind = models.CharField(
        max_length=100,
        choices=(("cat", "Cat"), ("dog", "Dog"))
    )

    def __str__(self):
        return self.name
