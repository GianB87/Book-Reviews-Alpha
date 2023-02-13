# Generated by Django 3.2.6 on 2021-08-14 02:56

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210813_2249'),
        ('posts', '0002_auto_20210810_1929'),
        ('books', '0004_auto_20210810_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewBook',
            fields=[
                ('body', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('value', models.CharField(choices=[('up', 'Up Vote'), ('down', 'Down Vote')], max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'unique_together': {('owner', 'post')},
            },
        ),
    ]