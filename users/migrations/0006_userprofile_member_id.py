import uuid
from django.db import migrations, models


def generate_user_id():
    return f"SKB-{uuid.uuid4().hex[:8].upper()}"


def populate_member_ids(apps, schema_editor):
    UserProfile = apps.get_model('users', 'UserProfile')
    existing_ids = set()
    for profile in UserProfile.objects.all():
        new_id = generate_user_id()
        while new_id in existing_ids:
            new_id = generate_user_id()
        existing_ids.add(new_id)
        profile.member_id = new_id
        profile.save(update_fields=['member_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userprofile_managed_airline'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='member_id',
            field=models.CharField(
                editable=False,
                max_length=12,
                null=True,
                verbose_name='Mã định danh (User ID)',
            ),
        ),
        migrations.RunPython(populate_member_ids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='userprofile',
            name='member_id',
            field=models.CharField(
                default=generate_user_id,
                editable=False,
                max_length=12,
                unique=True,
                verbose_name='Mã định danh (User ID)',
            ),
        ),
    ]
