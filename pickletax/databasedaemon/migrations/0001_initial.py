# Generated by Django 2.2 on 2019-05-13 19:22

import databasedaemon.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(max_length=100, validators=[databasedaemon.models.city_validator])),
                ('address', models.CharField(max_length=100)),
                ('info', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('number', models.CharField(max_length=20, primary_key=True, serialize=False, validators=[databasedaemon.models.classroom_number_validator])),
                ('seat_number', models.IntegerField(validators=[databasedaemon.models.classroom_seat_number_validator])),
                ('access_rights', models.CharField(choices=[('free', 'free'), ('teacher is required', 'teacher is required'), ('for stuff only', 'for stuff only')], default='free', max_length=20)),
                ('type', models.CharField(choices=[('lecture', 'lecture'), ('seminary', 'seminary'), ('laboratory', 'laboratory'), ('for stuff', 'for stuff')], default='seminary', max_length=20)),
                ('info', models.CharField(blank=True, max_length=500)),
                ('campus_ID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databasedaemon.Campus')),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('class_type', models.CharField(choices=[('simple class', 'simple class'), ('doubled class', 'doubled class')], default='doubled class', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.CharField(max_length=100, validators=[databasedaemon.models.mail_validator])),
                ('good_faith_index', models.IntegerField()),
                ('status', models.CharField(choices=[('student', 'student'), ('teacher', 'teacher'), ('redactor', 'redactor'), ('server', 'server')], default='student', max_length=20)),
                ('main_campus_ID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databasedaemon.Campus')),
            ],
        ),
        migrations.CreateModel(
            name='ClassroomActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(validators=[databasedaemon.models.class_number_validator])),
                ('vacant', models.CharField(choices=[('free', 'free'), ('reserved', 'reserved'), ('occupied', 'occupied')], default='free', max_length=20)),
                ('info', models.CharField(blank=True, max_length=500)),
                ('campus_ID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databasedaemon.Campus')),
                ('classroom_umber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databasedaemon.Classroom')),
            ],
        ),
        migrations.AddField(
            model_name='campus',
            name='institution_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databasedaemon.Institution'),
        ),
    ]
