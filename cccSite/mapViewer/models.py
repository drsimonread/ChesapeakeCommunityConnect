from django.db import models
from account.models import Member
from django.urls import reverse



class MapTag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    def __str__(self):
        return self.name

# this will be the ideal post model. we would serialize this to widgets using djangos JSON serialize functionality on the specific fields
class MapPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    description = models.TextField() #will be derived from content. whenever this stuff gets working.
    geoCode = models.JSONField()
    tags = models.ManyToManyField(MapTag, related_name="posts", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    visible_options = (
        (-1,"denied"),
        (0, "pending"),
        (1 , "visible"),
    )
    visibility = models.SmallIntegerField(default=0, choices=visible_options)
    def __str__(self):
        return self.title + " by " + str(self.author)
    @property
    def get_absolute_url(self):
        return reverse("mapViewer:post_detail", args=[str(self.pk)])


class PostComment(models.Model):
    post = models.ForeignKey(MapPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="post_comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies",
        null=True, blank=True,
    )
    content = models.TextField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    #https://forum.djangoproject.com/t/url-template-tag-get-absolute-url-and-views/21249
    #https://levelup.gitconnected.com/django-quick-tips-get-absolute-url-1c22321f806b
