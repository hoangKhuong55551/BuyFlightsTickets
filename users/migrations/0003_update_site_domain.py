"""
Data migration: Cập nhật domain trong django_site cho Render deployment.
Chạy tự động khi `python manage.py migrate`.
"""
from django.db import migrations


def update_site_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    import os
    # Trên Render, RENDER_EXTERNAL_URL có dạng https://skybook-yfwg.onrender.com
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if render_url:
        domain = render_url.replace("https://", "").replace("http://", "").strip("/")
    else:
        domain = "127.0.0.1:8000"

    Site.objects.update_or_create(
        id=1,
        defaults={"domain": domain, "name": "SkyBook"}
    )


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("users", "0002_newslettersubscriber_alter_userprofile_options_and_more"),
    ]

    operations = [
        migrations.RunPython(update_site_domain, migrations.RunPython.noop),
    ]
