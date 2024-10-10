"""
    Modèle de données pour les produits
"""
from django.db import models


PRODUCT_STATUS = ((0, 'Offline'), (1, 'Online'), (2, 'Out of stock'))

# Create your models here.
"""
    Status : numero, libelle
"""


class Status(models.Model):
    numero = models.IntegerField()
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.numero} - {self.libelle}"


class Product(models.Model):
    """
    Modèle de données pour les produits

    Attributs:
        name : Nom du produit
        code : Code du produit
        status : Statut du produit
        date_creation : Date de création du produit


    Méthodes:

    __str__ : Retourne le nom et le code du produit

    """

    class Meta:
        verbose_name = "Produit"

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    status = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation = models.DateTimeField(blank=True,
                                         verbose_name="Date création")
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.code}"


class ProductItem(models.Model):
    """
    Modèle de données pour les déclinaisons de produits
    """

    class Meta:
        verbose_name = "Déclinaison Produit"

    color = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attributes = models.ManyToManyField("ProductAttributeValue",
                                        related_name="product_item",
                                        null=True,
                                        blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.code}"


class ProductAttribute(models.Model):
    """
    Attributs produit
    """

    class Meta:
        verbose_name = "Attribut"

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """
    Valeurs des attributs
    """

    class Meta:
        verbose_name = "Valeur attribut"
        ordering = ['position']

    value = models.CharField(max_length=100)
    product_attribute = models.ForeignKey('ProductAttribute',
                                          verbose_name="Unité",
                                          on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField("Position",
                                                null=True,
                                                blank=True)

    def __str__(self):
        return f"{self.product_attribute.name} - {self.value}"


class Fournisseur(models.Model):
    """
    Représente les fournisseurs de produit
    """
    name = models.CharField(max_length=100)
    products = models.ManyToManyField("Product",
                                      through="Fournit",
                                      related_name="fournisseurs")

    def __str__(self):
        return self.name


class Fournit(models.Model):
    """
    Modèle de données pour la relation entre les fournisseurs et les produits

    Attributs:
        product : Produit fourni
        fournisseur : Fournisseur du produit
        price_ht : Prix unitaire HT
        price_ttc : Prix unitaire TTC

    Méthodes:

        __str__ : Retourne le nom du fournisseur, le nom du produit, le prix HT et le prix TTC
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)
    price_ht = models.DecimalField(max_digits=8,
                                   decimal_places=2,
                                   verbose_name="Prix unitaire HT")
    price_ttc = models.DecimalField(max_digits=8,
                                    decimal_places=2,
                                    verbose_name="Prix unitaire TTC")

    def __str__(self):
        return f"{self.fournisseur.name} fournit {self.product.name} à {self.price_ht} HT et {self.price_ttc} TTC"

class Commande(models.Model):
    """
    Modèle de données pour la relation entre les commandes, les produits et les fournisseurs

    Attributs:
        product : Produit commandé
        fournisseur : Fournisseur du produit
        user : Utilisateur qui a passé la commande
        quantity : Quantité commandée
        date_commande : Date de la commande
        status : Statut de la commande (en préparation, passée, reçue)

    Méthodes:

        __str__ : Retourne le nom de l'utilisateur, le nom du produit, la quantité et la date de la commande
    """
    STATUS_CHOICES = (
        (0, 'En préparation'),
        (1, 'Passée'),
        (2, 'Reçue'),
    )

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_commande = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return f"{self.user.username} a commandé {self.quantity} de {self.product.name} chez {self.fournisseur.name} le {self.date_commande}"

    def save(self, *args, **kwargs):
        if self.status == 2:  # Commande reçue
            self.product.stock += self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def advance_status(self):
        if self.status < 2:
            self.status += 1
            self.save()