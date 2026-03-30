from mapViewer.models import MapTag

def update_maptags(apps, schema_editor):
    MapTag = apps.get_model('mapViewer', 'MapTag')

    old_tags = [
        "Marine",
        "Land",
        "Air",
        "Local",
        "Plants",
        "Animals"
    ]

    new_tags = [
        "Biodiversity & Conservation",
        "Community Development & Placemaking",
        "Economic Diversity & Local Innovation",
        "Cultural Heritage & Expression",
        "Sustainable Food Systems",
        "Community Education & Workshops",
        "Youth-Led Initiatives",
        "Social Action & Impact",
        "Racial Healing"
    ]

    # To remove old tags
    MapTag.objects.filter(name__in=old_tags).delete()

    # To add new tags
    for name in new_tags:
        MapTag.objects.get_or_create(name=name)

class migration(migrations.Migration):

    dependencies = [
        ('mapViewer', '0023_update_maptags' ),
    ]

    operations = [
        migrations.RunPython(update_maptags),
    ]