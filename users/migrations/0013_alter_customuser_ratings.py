# Generated by Django 4.2.1 on 2023-06-17 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_customuser_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='ratings',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]