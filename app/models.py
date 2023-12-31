from django.db import models


from djongo import models

class USER_details(models.Model):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')

    

    NORMAL_USER = 'Normal User'
    USER_TYPES = [
        (NORMAL_USER, 'Normal User'),
    ]
    usertype = models.CharField(max_length=20,choices=USER_TYPES,default=NORMAL_USER,editable=False)
    # username = models.CharField(max_length=138)
    email = models.EmailField()
    password = models.CharField(max_length=138)
    date_joined = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self._id)










