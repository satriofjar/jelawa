from django.db import models
from base.validators import validate_file_size

# Create your models here.
class IndexContent(models.Model):
    hero_title = models.CharField()
    hero_desc = models.TextField()
    hero_sec_desc = models.TextField()

    sec_title = models.CharField()
    th_title = models.CharField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_content_box(self):
        return self.contenxtbox_set.all()

class ContenxtBox(models.Model):
    index_content = models.ForeignKey(IndexContent, on_delete=models.CASCADE)
    title = models.CharField()
    desc = models.TextField()
    img = models.ImageField(validators=[validate_file_size])


    @property
    def imageURL(self):
        try :
            url = self.img.url
        except:
            url = ''
        return url

    def __str__(self): 
        return str(self.title)

class MapsContent(models.Model):
    maps_title = models.CharField()
    maps_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class NavbarFooter(models.Model):
    icon = models.ImageField(validators=[validate_file_size])
    footer_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def iconURL(self):
        try :
            url = self.icon.url
        except:
            url = ''
        return url

    def __str__(self): 
        return str(self.footer_desc)
