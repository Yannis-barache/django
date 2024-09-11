from django.db import models
from django.utils import timezone

class Statut(models.Model):

    num = models.IntegerField()
    libelle = models.CharField(max_length=100)

    def __unicode__(self):
        return "Lib : {0}".format(self.libelle)

class Product(models.Model):
        name = models.CharField(max_length=100)
        code = models.IntegerField()
        price = models.FloatField()
        date_fabrication = models.DateField(auto_now_add=True)
        statut = models.ForeignKey(Statut, on_delete=models.CASCADE)



        def __unicode__(self):
            return "{0} [{1}]".format(self.name, self.code)

class ProductItem(models.Model):
        color = models.CharField(max_length=100)
        product = models.ForeignKey(Product, on_delete=models.CASCADE)

        def __unicode__(self):
            return "{0} {{1}} [{2}]".format(self.color, self.product.name, self.code)




