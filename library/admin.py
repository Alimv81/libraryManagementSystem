from django.contrib import admin

from library.models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(BorrowRecord)
