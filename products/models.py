import datetime  # Importa o módulo datetime do Python

from django.core.validators import MinValueValidator  # Importa o validador MinValueValidator do Django
from django.db import models  # Importa o módulo models do Django
# Create your models here.
from django.utils.text import slugify  # Importa a função slugify do módulo utils.text do Django

from categories.models import Category  # Importa o modelo Category do aplicativo categories
from shared.models import TimestampedModel  # Importa o modelo TimestampedModel do módulo shared
from tags.models import Tag  # Importa o modelo Tag do aplicativo tags

# Define um novo modelo chamado Product que herda de TimestampedModel
class Product(TimestampedModel):
    name = models.CharField(blank=False, null=False, max_length=200)  # Define um campo de caractere obrigatório para o nome
    slug = models.CharField(blank=False, null=False, max_length=100)  # Define um campo de caractere obrigatório para o slug
    description = models.TextField(blank=False, null=False)  # Define um campo de texto obrigatório para a descrição
    price = models.FloatField(validators=[MinValueValidator(0.1)])  # Define um campo de ponto flutuante para o preço com um validador de valor mínimo
    publish_on = models.DateTimeField(blank=True, null=True)  # Define um campo de data e hora opcional para a data de publicação
    tags = models.ManyToManyField(
        Tag, related_name='products'  # Define um relacionamento muitos para muitos com o modelo Tag

    )
    categories = models.ManyToManyField(
        Category, related_name='products'  # Define um relacionamento muitos para muitos com o modelo Category
    )
    stock = models.IntegerField(validators=[MinValueValidator(0)])  # Define um campo de inteiro para o estoque com um validador de valor mínimo

    # Sobrescreve o método save para customizar a lógica de salvamento
    def save(self, slug="", *args, **kwargs):
        if not self.publish_on:
            self.publish_on = datetime.datetime.now()  # Define a data de publicação como a data e hora atuais se não estiver definida
        if not self.slug:
            self.slug = slugify(self.name)  # Define o slug com base no nome se não estiver definido
        return super(Product, self).save(*args, **kwargs)  # Chama o método save da classe pai para concluir o salvamento
