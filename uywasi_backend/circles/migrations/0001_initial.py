# Generated by Django 3.0.5 on 2020-05-19 19:11

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
            name='Circle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on wich the object was created.')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on wich the object was last modified.')),
                ('name', models.CharField(help_text='This is the name of circle, but not is an identificator.', max_length=64)),
                ('slugname', models.SlugField(error_messages={'unique': 'A circle with this slugname already exists.'}, help_text='This name is the identificator of circle, do not repleace to ID field.', max_length=32, unique=True)),
                ('profile_photo', models.ImageField(blank=True, help_text='Photo of circle profile.', null=True, upload_to='circles/profile_pictures/')),
                ('cover_photo', models.ImageField(blank=True, help_text='Photo of circle cover.', null=True, upload_to='circles/cover_pictures/')),
                ('about', models.TextField(blank=True, help_text='Description of the circle.', null=True)),
                ('is_verified', models.BooleanField(default=False, help_text="An circle is verified only when the circle's identity was confirmed by staff.")),
                ('is_active', models.BooleanField(default=True, help_text='An circle is actived by default, but it change when the circle is eliminated.')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': ['-created', '-modified'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on wich the object was created.')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on wich the object was last modified.')),
                ('is_admin', models.BooleanField(blank=True, default=False, help_text='A user can post on a circle only if this field is True. This field is False by default, but the circle creator can switch this value to True.')),
                ('circle', models.ForeignKey(help_text='This is the circle which the user subcribed.', on_delete=django.db.models.deletion.CASCADE, to='circles.Circle')),
                ('user', models.ForeignKey(help_text='This is the user subscribed.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': ['-created', '-modified'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='circle',
            name='subscriptions',
            field=models.ManyToManyField(help_text='Group of users that are subscripted to this circle.', through='circles.Subscription', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'circle'), name='unique_user_circle'),
        ),
    ]
