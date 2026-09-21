from mapViewer.models import MapTag

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



for name in new_tags:
    MapTag.objects.get_or_create(name=name)

print("MapTag table updated.")