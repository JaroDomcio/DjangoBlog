from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager): #Menedżer opublikowanych postów
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)




class Post(models.Model): #model postu

    class Status(models.TextChoices): #Zapisywanie blogów jako wersji roboczej
        DRAFT = 'DF', 'Roboczy'
        PUBLISHED = 'PB', 'Opublikowany'

    title = models.CharField(max_length=250) #Pole posta
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts') 
    body = models.TextField() #zawiera treść posta
    publish = models.DateTimeField(default=timezone.now) #Data opublikowania posta
    created = models.DateTimeField(auto_now_add=True) #Data utworzenia posta
    updated = models.DateTimeField(auto_now=True) #Data aktualizowania posta
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    object = models.Manager() #Menedżer domyślny
    published = PublishedManager() # Niestandardowy menedżer opublikowanych postów

    tags = TaggableManager()
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering= ['-publish'] # Posty na blogu pokazują się w odwróconej chronologii
        indexes = [
            models.Index(fields=['-publish']) # Dodawanie indeksu do baz danych dla postów
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']) ]

    def __str__(self):
        return f'Komentarz dodany przez {self.name} dla posta {self.post}'