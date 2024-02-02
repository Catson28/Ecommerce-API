from django.db import models  # Importa o módulo models do Django
from shared.models import TimestampedModel  # Importa o modelo TimestampedModel de um módulo compartilhado
from users.models import AppUser  # Importa o modelo AppUser do módulo users.models

class Address(TimestampedModel):  # Define um novo modelo chamado Address que herda de TimestampedModel
    user = models.ForeignKey(AppUser,related_name='addresses',null=True,blank=True,on_delete=models.SET_NULL, verbose_name='User')  # Define um campo de chave estrangeira que se relaciona com o modelo AppUser
    first_name = models.CharField(blank=False, max_length=50)  # Define um campo de caractere para o primeiro nome, não pode ser em branco, no máximo 50 caracteres
    last_name = models.CharField(blank=False, max_length=50)  # Define um campo de caractere para o sobrenome, não pode ser em branco, no máximo 50 caracteres
    country = models.CharField(blank=False, max_length=50)  # Define um campo de caractere para o país, não pode ser em branco, no máximo 50 caracteres
    city = models.CharField(blank=False, max_length=50)  # Define um campo de caractere para a cidade, não pode ser em branco, no máximo 50 caracteres
    address = models.CharField(blank=False, max_length=50)  # Define um campo de caractere para o endereço, não pode ser em branco, no máximo 50 caracteres
    zip_code = models.CharField(blank=False, max_length=20)  # Define um campo de caractere para o código postal, não pode ser em branco, no máximo 20 caracteres
