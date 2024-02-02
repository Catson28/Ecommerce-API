from django.db import models  # Importa o módulo models do Django
from django.utils.text import slugify  # Importa a função slugify do Django
from shared.models import TimestampedModel  # Importa o modelo TimestampedModel de um módulo compartilhado

class CategoryManager(models.Manager):

    def gent_random_category(self):
        return Category.objects.order_by('?').first()  # Gera e retorna uma categoria aleatória

class Category(TimestampedModel):  # Define um novo modelo chamado Category que herda de TimestampedModel
    name = models.CharField(max_length=255)  # Define um campo de caractere para o nome da categoria, com no máximo 255 caracteres
    slug = models.SlugField(db_index=True, unique=True)  # Define um campo de slug para a URL amigável, com índice no banco de dados e exclusividade
    description = models.CharField(max_length=140)  # Define um campo de caractere para a descrição da categoria, com no máximo 140 caracteres

    objects = CategoryManager()  # Atribui um gerenciador de objetos personalizado chamado CategoryManager a este modelo

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  # Gera automaticamente um slug baseado no nome da categoria ao salvar
        return super(Category, self).save(*args, **kwargs)  # Chama o método save da classe pai (TimestampedModel)

    def __str__(self):
        return self.name  # Retorna o nome da categoria como representação de string para facilitar a visualização
