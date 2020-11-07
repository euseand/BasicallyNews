from django.db import models


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Contact instance: ' + self.name + ' - ' + self.email + ' - ' + self.time_stamp.strftime("%d/%m/%Y, "
                                                                                                        "%H:%M:%S")
