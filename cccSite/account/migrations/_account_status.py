from django.db import migrations
from django.db.migrations.recorder import MigrationRecorder


class AddAccountStatus(migrations.AddField):
    """The two historical account migration branches share one status column."""

    def __init__(self, field, other_migration):
        super().__init__(model_name="accountcreation", name="status", field=field)
        self.other_migration = other_migration

    def deconstruct(self):
        return self.__class__.__name__, [], {
            "field": self.field,
            "other_migration": self.other_migration,
        }

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.model_name)
        connection = schema_editor.connection
        if not self.allow_migrate_model(connection.alias, model):
            return

        with connection.cursor() as cursor:
            columns = connection.introspection.get_table_description(cursor, model._meta.db_table)
        if all(column.name != self.name for column in columns):
            super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        recorded = MigrationRecorder(schema_editor.connection).migration_qs
        if not recorded.filter(app=app_label, name=self.other_migration).exists():
            super().database_backwards(app_label, schema_editor, from_state, to_state)
