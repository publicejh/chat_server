from django.db import models


class Contact(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=150)
    # friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return '{}'.format(self.user_id)


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    is_file = models.BooleanField(default=False)
    file_path = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.contact.user_id)


class Chat(models.Model):
    name = models.TextField()
    sig_id = models.IntegerField()
    participants = models.ManyToManyField(Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return '{}'.format(self.pk)

    def group_name(self):
        return 'chat_%s' % self.pk
