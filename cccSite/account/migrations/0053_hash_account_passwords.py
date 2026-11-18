from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password
from django.db import migrations, models


def hash_account_passwords(apps, schema_editor):
    AccountCreation = apps.get_model("account", "AccountCreation")
    accounts = AccountCreation.objects.using(schema_editor.connection.alias)
    hasher = BCryptSHA256PasswordHasher()
    for account in accounts.only("password").order_by("pk").iterator():
        account.password = make_password(account.password, hasher=hasher)
        account.save(update_fields=["password"])


class Migration(migrations.Migration):
    dependencies = [("account", "0052_alter_member_ranking")]

    operations = [
        migrations.AlterField(
            model_name="accountcreation",
            name="password",
            field=models.CharField(editable=False, max_length=128),
        ),
        migrations.RunPython(hash_account_passwords),
        migrations.RemoveField(model_name="accountcreation", name="confirmpassword"),
    ]
