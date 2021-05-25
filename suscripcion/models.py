from django.db import models
# Create your models here.



class SuscripcionUsuario(models.Model):
    numero_id = models.AutoField(primary_key=True, unique=True, editable=False)
    email = models.EmailField()
    create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email



class SuscripcionControl(models.Model):
    EMAIL_STATUS_CHOICES = (
        ('Borrador', 'Borrador'),
        ('Publicado', 'Publicado')
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    email = models.ManyToManyField(SuscripcionUsuario)
    imagen = models.ImageField()
    status = models.CharField(max_length=10, choices=EMAIL_STATUS_CHOICES)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


        