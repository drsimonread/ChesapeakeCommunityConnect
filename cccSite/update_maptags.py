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


tag_colors = {
    "Biodiversity & Conservation": "#4CAF50",
    "Community Development & Placemaking": "#FF9800",
    "Economic Diversity & Local Innovation": "#2196F3",
    "Cultural Heritage & Expression": "#9C27B0",
    "Sustainable Food Systems": "#FFEB3B",
    "Community Education & Workshops": "#00BCD4",
    "Youth-Led Initiatives": "#E91E63",
    "Social Action & Impact": "#F44336",
    "Racial Healing": "#795548",
}

for name in new_tags:
    MapTag.objects.get_or_create(
        name=name,
        defaults={"color": tag_colors.get(name, "#4285F4")},
    )

print("MapTag table updated.")