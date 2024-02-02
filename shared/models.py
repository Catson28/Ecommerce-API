from django.db import models  # Importa o módulo models do Django

# Define um modelo abstrato chamado TimestampedModel
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Campo para armazenar a data e hora de criação (auto_now_add garante que seja definido apenas uma vez na criação)
    updated_at = models.DateTimeField(auto_now=True)  # Campo para armazenar a data e hora da última atualização (auto_now garante que seja atualizado automaticamente)

    class Meta:
        abstract = True  # Indica que este é um modelo abstrato e não deve ser usado para criar tabelas no banco de dados

        # Por padrão, qualquer modelo que herde de `TimestampedModel` deve
        # ser ordenado em ordem cronológica reversa. Podemos substituir isso em uma
        # base de modelo específica conforme necessário, mas a ordem cronológica reversa é uma
        # boa ordenação padrão para a maioria dos modelos.
        ordering = ['-created_at', '-updated_at']  # Define a ordem padrão como reversa cronológica

