# Generated by Django 3.0.11 on 2021-01-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0003_apicall_api_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
    ]