from django.urls import path
from catalog import views

# path defines :
#  URL pattern which in this case is empty string ''
#  a view function that will be called if the URL pattern is detected 
#   (views.index which refers to index() in views.py)
#  name refers to the specific URL mapping
# Path function: path('url_pattern/', view_function(), name = 'object_name')


urlpatterns = [
	path('', views.index, name='index'),
	path('books/', views.BookListView.as_view(), name='books'),
	# URL for specific book details
	# <variable> is the syntax used for getting a variable from the model
	# <int:pk> means the variable pk (primary key in book model) is being captured as an int
	path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
	path('authors/', views.AuthorListView.as_view(), name='authors'),
	path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
	path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
	path('borrowedbooks/', views.LoanedBooksListView.as_view(), name='all-borrowed'),
]

urlpatterns += [
	path('book/<uuid:pk>/renew', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
	path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
	path('author/<int:pk>/update', views.AuthorUpdate.as_view(), name='author_update'),
	path('author/<int:pk>/delete', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
	path('book/create/', views.BookCreate.as_view(), name='book-create'),
	path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
	path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
] 