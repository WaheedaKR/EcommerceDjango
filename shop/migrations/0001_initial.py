# Generated by Django 3.1 on 2023-04-14 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_item', models.CharField(max_length=200, unique=True)),
                ('url_item', models.SlugField(max_length=200, unique=True)),
                ('description_item', models.TextField(blank=True, max_length=500)),
                ('cost', models.IntegerField()),
                ('picture', models.ImageField(upload_to='pictures/items')),
                ('stock_item', models.IntegerField()),
                ('availability', models.BooleanField(default=True)),
                ('date_of_item_created', models.DateTimeField(auto_now_add=True)),
                ('date_of_item_modified', models.DateTimeField(auto_now=True)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.categories')),
            ],
        ),
    ]
