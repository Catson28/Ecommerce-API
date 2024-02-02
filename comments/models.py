from django.db import models  # Importa o módulo models do Django

# Importa os modelos necessários para a relação com este modelo
from products.models import Product  # Importa o modelo Product do aplicativo products
from shared.models import TimestampedModel  # Importa o modelo TimestampedModel do módulo shared
from users.models import AppUser  # Importa o modelo AppUser do aplicativo users

# Define um novo modelo chamado Comment que herda de TimestampedModel
class Comment(TimestampedModel):
    content = models.TextField()  # Define um campo de texto para o conteúdo do comentário
    rating = models.IntegerField(null=True, blank=True)  # Define um campo de inteiro para a classificação do comentário (pode ser nulo e em branco)
    product = models.ForeignKey(Product, related_name='comments', null=True, blank=True, on_delete=models.CASCADE)  # Define um campo de chave estrangeira para o modelo Product
    user = models.ForeignKey(AppUser, related_name='comments', on_delete=models.CASCADE)  # Define um campo de chave estrangeira para o modelo AppUser
