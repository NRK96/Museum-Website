# Generated by Django 2.0.2 on 2018-05-10 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0002_docent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='docent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.Docent'),
        ),
    ]