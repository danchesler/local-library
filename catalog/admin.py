from django.contrib import admin

# Register your models here.

from catalog.models import Author, Genre, Book, BookInstance, Language

# Inline class to view books author has written at an author's page
class BookAuthorInstanceInline(admin.TabularInline):
	model = Book
	extra = 0

# Model admin class for author
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	# fields attribute lists the fields that are to be displayed on the form
	fields = ('first_name', 'last_name', ('date_of_birth', 'date_of_death'))
	inlines = [BookAuthorInstanceInline]
admin.site.register(Author, AuthorAdmin)


# Inline class to view instances of books at a book's page
class BooksInstanceInline(admin.TabularInline):
	model = BookInstance
	extra = 0 #removes display of spare book instances

# Model admin class for book
# Registered using a decorator.
# Using a decorator does the exact same thing as 
# admin.site.register(Book, BookAdmin)
# display_genre function is used because you cannot refer to many-to-many objects
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	# borrow is for User borrowing a book instance
	list_display = ('display_title', 'status', 'borrower','due_back', 'id')
	# creates a list of filter options based on given fields
	list_filter = ('status', 'due_back')

	fieldsets = (
		(None, {
			'fields' : ('book', 'imprint', 'id')
		}),
		('Availability', {
			'fields' : ('status', 'due_back', 'borrower')
		}),
	)

#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Language)
