# Generated by Django 4.1.7 on 2023-03-26 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_avatar_alter_account_user_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_pic', verbose_name='Аватар'),
        ),
    ]
