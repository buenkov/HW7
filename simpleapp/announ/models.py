from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
class Announcement(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Player, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)# добавим переводящийся текст подсказку к полю)
    category = models.ForeignKey(Category, unique=False, null=False, on_delete=models.CASCADE)
    content = RichTextField(null=False,)

    def __str__(self):
          s= f"{self.title}, от {self.create_date.strftime('%d %b %Y')} "
          return s



class Response(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    announcement_id = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    text = models.TextField(default ='')
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
                              default='pending')
    def __str__(self):
        return f"{self.player_id} | отклик на ,{self.announcement_id}."

class News(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title