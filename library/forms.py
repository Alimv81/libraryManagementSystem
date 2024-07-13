from django import forms
from . import models as lib_models


class BookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    copies = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    isbn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = lib_models.Book
        fields = ('title', 'copies', 'isbn')

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        books_with_same_title = lib_models.Book.objects.filter(title__iexact=title)
        if self.instance:
            books_with_same_title = books_with_same_title.exclude(pk=self.instance.pk)
        if books_with_same_title.exists():
            raise forms.ValidationError('Book with same title is already taken')
        return title

    def clean_copies(self, *args, **kwargs):
        copies = self.cleaned_data.get('copies')
        if copies > 0:
            return copies
        else:
            raise forms.ValidationError(None, 'Number of copies cannot be zero')

    def clean_isbn(self, *args, **kwargs):
        isbn = self.cleaned_data.get('isbn')
        books_with_same_isbn = lib_models.Book.objects.filter(isbn=isbn)
        if self.instance:
            books_with_same_isbn = books_with_same_isbn.exclude(pk=self.instance.pk)
        if books_with_same_isbn.exists():
            raise forms.ValidationError(None, 'Book with this ISBN already exists')
        for ch in isbn:
            if not ch.isdigit():
                raise forms.ValidationError(None, 'Invalid ISBN')
        return isbn





