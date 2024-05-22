import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .models import BorrowRecord


# Create your views here.
@login_required(login_url='accounts:login', redirect_field_name='')
def index(request):
    return render(request, 'library/index.html', {})


def about(request):
    return render(request, 'library/about.html', {})


@login_required(login_url='accounts:login', redirect_field_name='')
def profile(request):
    user = request.user
    member = models.Member.objects.get(user=user)
    borrows = models.BorrowRecord.objects.filter(member=member, return_date=None)
    return render(request, 'library/profile.html', {'member': member, 'borrows': borrows})


@login_required(login_url='accounts:login', redirect_field_name='')
def show_books(request):
    available_books = models.Book.objects.filter(book__copies__gt=0)
    return render(request, 'library/show_books.html', {'available_books': available_books})


@login_required(login_url='accounts:login', redirect_field_name='')
def borrow_book(request, book_id):
    book = get_object_or_404(models.Book, pk=book_id)
    if request.method == 'POST':
        book.copies -= 1
        member = models.Member.objects.get(user=request.user)
        borrow = BorrowRecord(book=book, member=member,
                              return_date=None)
        borrow.save()
        return redirect('library:index')
    else:
        pass
    return render(request, 'library/confirm_take_book.html', {'book': book})
