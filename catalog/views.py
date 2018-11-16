from django.shortcuts import render
# render() generates HTML using a template and data

from catalog.models import Book, Author, BookInstance, Genre, Language

# View function for the homepage
def index(request):
	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# The 'all()' is implied by default
	num_authors = Author.objects.count()

	# Visit count per session, set to 0 by default if value doesn't exist
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	# Counts of genre
	num_genres = Genre.objects.all().count()

	# Counts of books with a particular word
	word_filter = 'the'
	#num_books_word = Book.objects.filter(title__contains='the').count()
	num_books_word = Book.objects.filter(title__icontains=word_filter).count()

	context = {
		'num_books' : num_books,
		'num_instances' : num_instances_available,
		'num_instances_available' : num_instances_available,
		'num_authors' : num_authors,
		'num_visits' : num_visits,
		'num_genres' : num_genres,
		'num_books_word' : num_books_word,
		'word_filter' : word_filter,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)

# Class-based view for books
from django.views import generic

class BookListView(generic.ListView):
	model = Book
	paginate_by = 2 #Only display 10 books at a time

# Class-based view for book detail
class BookDetailView(generic.DetailView):
	model = Book

class AuthorListView(generic.ListView):
	model = Author

# Need to access book model in the author detail view
class AuthorDetailView(generic.DetailView):
	model = Author

from django.contrib.auth.mixins import LoginRequiredMixin

# Generic class-based view listing books loaned to current user
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	# Restrict the query to only list BookInstance objects for current user
	# 'o' is the stored code for 'on loan'
	# ordered by due_back date so oldest items are displayed first
	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
	permission_required = 'catalog.can_view_borrowed'
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed.html'
	paginate_by = 10

	# Filter set of book instances to only ones that are on loan
	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')


import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
	"""View function for renewing a specific BookInstance by librarian."""
	book_instance = get_object_or_404(BookInstance, pk=pk)

	# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate with data from the request (binding):
		book_renewal_form = RenewBookForm(request.POST)

		# Check if form is valid
		if book_renewal_form.is_valid():
			# process the data in form.cleaned_data as required
			# (here we just write it to the model due_back field)
			book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
			book_instance.save()			

			#redirect to a new URL:
			return HttpResponseRedirect(reverse('all-borrowed'))

	# If this is a GET (or any other method) create the default form
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

	context = {
		'form' : book_renewal_form,
		'book_instance' : book_instance,
	}

	return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

# Views for author creation
class AuthorCreate(CreateView):
	model = Author
	fields = '__all__'
	initial = { 'date_of_birth': '05/01/2018' } # specify initial value

class AuthorUpdate(UpdateView):
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
	model = Author
	success_url = reverse_lazy('authors') # redirect to author list

# Views for book creation
class BookCreate(CreateView):
	model = Book
	fields = '__all__'

class BookUpdate(UpdateView):
	model = Book
	fields = '__all__'

class BookDelete(DeleteView):
	model = Book
	success_url = reverse_lazy('books') # redirect to book list