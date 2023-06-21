# Generated by Django 4.2.1 on 2023-05-31 13:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'gender',
                'verbose_name_plural': 'genders',
                'ordering': ['name'],
                'permissions': (('can_view_gender', 'Can view gender'), ('can_add_gender', 'Can add gender'), ('can_edit_gender', 'Can edit gender'), ('can_delete_gender', 'Can delete gender')),
                'default_related_name': 'genders',
                'indexes': [models.Index(fields=['id', 'name'], name='users_gende_id_510b3c_idx')],
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=14, unique=True)),
                ('otp_code', models.CharField(blank=True, max_length=6, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.gender')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ['-created_at'],
                'permissions': (('can_view_user', 'Can view user'), ('can_add_user', 'Can add user'), ('can_edit_user', 'Can edit user'), ('can_delete_user', 'Can delete user')),
                'default_related_name': 'users',
                'indexes': [models.Index(fields=['id', 'email', 'phone_number'], name='users_custo_id_cb84dd_idx')],
                'unique_together': {('email', 'phone_number')},
            },
        ),
    ]