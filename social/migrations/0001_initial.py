# Generated by Django 4.0.4 on 2022-04-19 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=25, null=True)),
                ('profile_pic', models.ImageField(default='uploads/profile_pictures/default-blue.png', upload_to='uploads/profile_pictures')),
                ('banner_pic', models.ImageField(default='740377.png', upload_to='uploads/banner_pictures')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]