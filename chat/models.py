from django.db import models
from django.utils.text import slugify


class Room(models.Model):
    name = models.CharField(max_length=255)
    label = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs) -> None:
        self.label = slugify(self.name)
        return super(Room, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.label

    def get_last_10_messages(self):
        return Message.objects.all()[:10]


class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return self.message
