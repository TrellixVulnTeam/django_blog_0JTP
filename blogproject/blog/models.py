from django.db import models
from django.contrib.auth.models import  User
from django.core.urlresolvers import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=300,blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_time','title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        if not self.excerpt :
          md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
          self.excerpt = strip_tags(md.convert(self.body))[:60]
        super(Post, self).save(*args,**kwargs)

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])




