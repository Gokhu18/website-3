# Generated by Django 2.1 on 2018-11-06 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_auto_20181106_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyer',
            old_name='Email',
            new_name='b_Email',
        ),
        migrations.RenameField(
            model_name='seller',
            old_name='Email',
            new_name='s_Email',
        ),
    ]
