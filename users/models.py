from django.contrib.auth.models import AbstractUser, UserManager  # Importa o modelo AbstractUser e o gerenciador UserManager do Django
from django.db import models  # Importa o módulo models do Django

# Create your models here.

# Define um novo gerenciador de usuário chamado AppUserManager que herda de UserManager
class AppUserManager(UserManager):

    # Método fictício para verificar se um comentário é confiável (não implementado)
    def is_trusty_comment(self):
        pass

    # Método para obter o primeiro usuário com a permissão de superusuário (admin)
    def get_admin(self):
        return UserManager.filter(self, is_superuser=True).first()

# Define um novo modelo de usuário chamado AppUser que herda de AbstractUser
class AppUser(AbstractUser):
    objects = AppUserManager()  # Atribui o gerenciador de objetos AppUserManager ao modelo
