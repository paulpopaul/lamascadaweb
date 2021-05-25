# Generated by Django 3.0.6 on 2021-05-24 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('estado', models.CharField(choices=[('Publicado', 'Publicado'), ('Borrador', 'Borrador')], default='Publicado', max_length=12)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('imagen', models.ImageField(upload_to='')),
                ('titulo', models.CharField(blank=True, max_length=255, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('numero_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Galeria de Imágenes',
            },
        ),
    ]
