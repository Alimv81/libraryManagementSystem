import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from . import models
from .forms import BookForm
from .models import BorrowRecord, Member


# Create your views here.
def about(request):
    return render(request, 'library/about.html', {})


@login_required(login_url='accounts:login', redirect_field_name='')
def index(request):
    user = request.user
    member = Member.objects.get(user=user)
    return render(request, 'library/index.html', {'member': member})


# member views:
@login_required(login_url='accounts:login', redirect_field_name='')
def borrowed_books(request):
    user = request.user
    member = models.Member.objects.get(user=user)
    borrows = models.BorrowRecord.objects.filter(member=member, return_date=None)
    context = {'member': member, 'borrows': borrows}
    return render(request, 'library/your books.html', context)


@login_required(login_url='accounts:login', redirect_field_name='')
def show_books(request):
    available_books = models.Book.objects.filter(copies__gt=0)
    return render(request, 'library/show_books.html', {'available_books': available_books})


@login_required(login_url='accounts:login', redirect_field_name='')
def borrow_book(request, pk):
    book = get_object_or_404(models.Book, pk=pk)
    book.copies -= 1
    book.save()
    member = models.Member.objects.get(user=request.user)
    borrow = BorrowRecord(book=book, member=member,
                          return_date=None)
    borrow.save()
    return redirect('library:index')


@login_required(login_url='accounts:login', redirect_field_name='')
def return_book(request, pk):
    book = get_object_or_404(models.Book, pk=pk)
    book.copies += 1
    book.save()
    member = models.Member.objects.get(user=request.user)
    borrow = BorrowRecord.objects.filter(member=member, book=book, return_date=None)
    borrow = borrow.first()
    borrow.return_date = datetime.date.today()
    borrow.save()
    return redirect('library:index')


# author views
@login_required(login_url='accounts:login', redirect_field_name='')
def written_books(request):
    user = request.user
    member = models.Member.objects.get(user=user)
    books = models.Book.objects.filter(author=member)
    return render(request, 'library/written books.html', {'written_books': books})


@login_required(login_url='accounts:login', redirect_field_name='')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(data=request.POST or None)
        if form.is_valid():
            member = models.Member.objects.get(user=request.user)
            title = form.cleaned_data['title']
            isbn = form.cleaned_data['isbn']
            copies = form.cleaned_data['copies']
            book = models.Book.objects.create(title=title, author=member, isbn=isbn, copies=copies)
            book.save()
            # form.save()
            return redirect('library:index')
        else:
            form.add_error(None, 'Invalid information')
            print(form.errors)
            return redirect('library:add_book')
    else:
        form = BookForm()
        return render(request, "library/add_book.html", {'form': form})


@login_required(login_url='accounts:login', redirect_field_name='')
def edit_book(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(models.Book, pk=pk)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library:index')
        else:
            print(form.errors)
            return redirect('library:edit_book', pk)
    book = get_object_or_404(models.Book, pk=pk)
    form = BookForm(instance=book)
    return render(request, 'library/edit_book.html',
                  {'form': form, 'pk': pk})


@login_required(login_url='accounts:login', redirect_field_name='')
def delete_book(request, pk):
    book = get_object_or_404(models.Book, pk=pk)
    book.delete()
    return redirect('library:index')
