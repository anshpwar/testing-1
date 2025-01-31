from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]

    operations = [
        migrations.RenameField(model_name="order", old_name="amount_cents", new_name="amount"),
    ]
