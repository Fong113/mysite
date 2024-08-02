from django.shortcuts import render
from .constants import get_loan_status, PAGINATE_BY, DEFAULT_DATE
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author
import datetime
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

class AuthorListView(generic.ListView):
  model = Author
  paginate_by = PAGINATE_BY

class BookDetailView(generic.DetailView):
  model = Book

class AuthorDetailView(generic.DetailView):
  model = Author

def book_detail_view(request, primary_key):
  book = get_object_or_404(Book, pk=primary_key)
  return render(request, 'catalog/book_detail.html', context={'book': book})

class LoanedBooksByUserListView(generic.ListView):
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by = PAGINATE_BY

  def get_queryset(self):
      return (
          BookInstance.objects.filter(borrower=self.request.user)
          .filter(status__exact=get_loan_status('On loan'))
          .order_by('due_back')
      )

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
  """View function for renewing a specific BookInstance by librarian."""
  book_instance = get_object_or_404(BookInstance, pk=pk)
  if request.method == 'POST':
    form = RenewBookForm(request.POST)
    if form.is_valid():
      book_instance.due_back = form.cleaned_data['renewal_date']
      book_instance.save()
      return HttpResponseRedirect(reverse('all-borrowed') )
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

  context = {
    'form': form,
    'book_instance': book_instance,
  }
  return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
  model = Author
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
  initial = {'date_of_death': DEFAULT_DATE }

class AuthorUpdate(UpdateView):
  model = Author
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
  model = Author
  success_url = reverse_lazy('authors')
