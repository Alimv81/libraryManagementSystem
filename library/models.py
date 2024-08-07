from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_date = models.DateField(auto_now_add=True)
    role = models.TextField(default='member')

    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('products:products-details', kwargs={'id': self.id})


class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.user.username} borrowed {self.book.title}"
