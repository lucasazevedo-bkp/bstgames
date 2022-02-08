from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_email_verified = models.BooleanField(_('verified email'), default=False, help_text=_('Designates whether the user verified the email and can log into this site.'))


class UserAddress(models.Model):
    STATE_CHOICES = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', ' Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), 
        ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', ' Mato Grosso do Sul'), ('MG', 'Minas Gerais'), 
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', ' Piauí'), 
        ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), 
        ('RR', 'Roraima'), ('SC', ' Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins') 
    )
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name='User')
    postal_code = models.CharField('Postal code', max_length=9, blank=True, validators=[MinLengthValidator(9)])
    state = models.CharField('State', max_length=2, blank=True, validators=[MinLengthValidator(2)], choices=STATE_CHOICES)
    locality = models.CharField('Locality', blank=True, max_length=50)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.postal_code
