from django.db import models

class Dt(models.Model):
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True, db_index=True)


    def __str__(self):
        return self.content
