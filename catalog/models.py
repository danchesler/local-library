from django.db import models
from django.contrib.auth.models import User
from datetime import date #Check dates for overdue books

# Model for book genre
# Has name field to define a genre name
class Genre(models.Model):
	name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Fantasy)')

	# Returns the name of the genre
	def __str__(self):
		return self.name

# Model representing language
class Language(models.Model):
	name = models.CharField(max_length=200, help_text='Enter a language (e.g. English, Nipponese, etc')

	def __str__(self):
		return self.name

# Model for representing a book
from django.urls import reverse # Used to generate URLs by reversing URL patterns

class Book(models.Model):
	title = models.CharField(max_length=200)
	
	# Foreign key for author. Author is a separate model
	# Book can only have one author. Author have multiple books
	# Author is a string rather than object because it hasn't been declared yet
	# ForeignKey defins a One-to-many relationship
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

	summary = models.TextField(max_length=1000, help_text='Enter a description for the book')
	isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

	# Many-to-many relationship to genre. Genre can contain many books. Books can be multiple genres.
	# Genre class has been defined so we can specify a Genre object
	genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

	# Challenge addition: language
	# Book and language have a One-to-many relationship
	language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

	# Create string for the genre to display it
	def display_genre(self):
		return ', '.join(genre.name for genre in self.genre.all()[:3])
	# short_description is a django tag for functions that will replace display names 
	# with a user-defined string
	display_genre.short_description = 'Genre'

	def __str__(self):
		return self.title

	# Returns a URL that can be used to access a detail record for this model
	def get_absolute_url(self): 
		return reverse('book-detail', args=[str(self.id)])

# Model for book instances
# Book instances represent a specific copy that has been borrowed
import uuid # Required for unique book instances

class BookInstance(models.Model):
	# id is the primary key of the BookInstance model
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True) #null for when book is available

	# FK for one-to-many relationship with User
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	# Tuple of tuple key-value pairs passed to 'choices' in status as an argument
	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	)

	# Defines book availability with LOAN_STATUS
	# Defines a choice/selection list
	status = models.CharField(
		max_length=1,
		choices=LOAN_STATUS,
		blank=True,
		default='m',
		help_text='Book availability'
	)

	# Meta class uses due_back field to order records when they're returned in a query
	class Meta:
		ordering = ['due_back']
		permissions = (("can_mark_returned", "Set book as returned"), ("can_view_borrowed", "View borrowed books"))

	def display_id(self):
		return self.id
	display_id.short_description = 'ID'

	def display_title(self):
		return self.book.title
	display_title.short_description = 'Book Title'

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False

	# Returns a formatted string that concatenated id and title
	# interpolates id and title to return value representated by each variable
	def __str__(self):
		return f'{self.id} ({self.book.title})'


# Model representing an author
class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('died', null=True, blank=True)

	class Meta:
		ordering = ['last_name', 'first_name']

	# Returns url to access specific author instance
	def get_absolute_url(self):
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'
