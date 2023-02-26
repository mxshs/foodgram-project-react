# Generated by Django 2.2.16 on 2023-02-26 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('measurement_unit', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('image', models.ImageField(upload_to='recipes/images/')),
                ('text', models.TextField()),
                ('cooking_time', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('color', models.TextField()),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='recipes_tag_name_56fd94_idx'),
        ),
    ]
