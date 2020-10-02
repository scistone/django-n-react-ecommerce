# Generated by Django 3.1.2 on 2020-10-02 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.URLField()),
                ('description', models.TextField(blank=True, null=True)),
                ('meta_url', models.CharField(max_length=255)),
                ('meta_desc', models.CharField(max_length=144)),
            ],
        ),
    ]