# Generated by Django 4.2.1 on 2023-06-02 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_country_options_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gender',
            options={'default_related_name': 'genders', 'ordering': ['name'], 'verbose_name': 'gender', 'verbose_name_plural': 'genders'},
        ),
    ]
