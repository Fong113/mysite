from django.shortcuts import render
from .constants import get_loan_status, PAGINATE_BY
from django.views import generic
from django.shortcuts import get_object_or_404

from catalog.models import Book, Author, BookInstance, Genre
def index(request):
  """View function for home page of site."""
  num_books = Book.objects.count()
  num_instances = BookInstance.objects.count()
  num_instances_available = BookInstance.objects.filter(status__exact=get_loan_status('Available')).count()
  num_authors = Author.objects.count()

  num_visits = request.session.get('num_visits', 1)
  request.session['num_visits'] = num_visits + 1

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_visits': num_visits,
  }
  return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
  model = Book
  queryset = Book.objects.select_related('author').all()
  paginate_by = PAGINATE_BY

  def get_context_data(self, **kwargs):
    context = super(BookListView, self).get_context_data(**kwargs)
    context['some_data'] = 'This is just some data'
    return context

class BookDetailView(generic.DetailView):
  model = Book

def book_detail_view(request, primary_key):
  book = get_object_or_404(Book, pk=primary_key)
  return render(request, 'catalog/book_detail.html', context={'book': book})
