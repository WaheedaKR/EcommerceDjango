# Generated by Django 4.2.1 on 2023-05-30 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_first_name_order_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='email',
            new_name='emailAddress',
        ),
    ]
