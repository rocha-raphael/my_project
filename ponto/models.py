from django.db import models

# Create your models here.
# models.py

class RegistroPonto(models.Model):
    ENTRADA_1 = 'E1'
    SAIDA_1 = 'S1'
    ENTRADA_2 = 'E2'
    SAIDA_2 = 'S2'

    PONTO_CHOICES = [
        (ENTRADA_1, 'Entrada 1'),
        (SAIDA_1, 'Saida 1'),
        (ENTRADA_2, 'Entrada 2'),
        (SAIDA_2, 'Saida 2'),
    ]

    nome_completo = models.CharField(max_length=255)
    horario = models.DateTimeField(auto_now_add=True)
    ponto = models.CharField(max_length=2, choices=PONTO_CHOICES)
    cpf = models.CharField(max_length=11, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nome_completo} - {self.get_ponto_display()}'
