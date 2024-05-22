from django import forms
from . import models as lib_models


class BookForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
    copies = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
    isbn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))

    class Meta:
        model = lib_models.Book
        fields = ('name', 'author', 'number_of_copies')

    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        taken_names = lib_models.Book.objects.filter(name__iexact=name)
        if taken_names:
            raise forms.ValidationError(None, 'Book with this name already exists')
        else:
            return name

    def clean_author(self, *args, **kwargs):
        author = self.cleaned_data.get('author')
        authors = lib_models.Author.objects.filter(name__iexact=author)
        if authors:
            return author
        else:
            raise forms.ValidationError(None, 'Author with this name does not exist')

    def clean_copies(self, *args, **kwargs):
        copies = self.cleaned_data.get('copies')
        if copies > 0:
            return copies
        else:
            raise forms.ValidationError(None, 'Number of copies cannot be zero')

    def clean_isbn(self, *args, **kwargs):
        isbn = self.cleaned_data.get('isbn')
        for ch in isbn:
            if not ch.isdigit():
                raise forms.ValidationError(None, 'Invalid ISBN')
        return isbn


class AuthorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))

    class Meta:
        model = lib_models.Author
        fields = ('name', 'email')

    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        taken_names = lib_models.Author.objects.filter(name__iexact=name)
        if taken_names:
            raise forms.ValidationError(None, 'Author with this name already exists')
        else:
            return name

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        emails = lib_models.Author.objects.filter(email__iexact=email)
        if emails:
            return forms.ValidationError(None, 'Author with this email already exists')
        else:
            return email
