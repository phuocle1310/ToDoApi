from django.db import models

# Create your models here.


class ToDoTask(models.Model):
    ids = models.CharField(max_length=100)
    task_name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.CharField(max_length=50, null=False)
    NEW = 'NEW'
    WORKING = 'WORKING'
    DONE = 'DONE'
    STATUS_CHOICES = (
        (NEW, 'NEW'),
        (WORKING, 'WORKING'),
        (DONE, 'DONE'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default=NEW)

    class Meta:
        ordering = ['-id']

    # def __str__(self):
    #     return self.task_name
