from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import requests
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
# import book model
from .models import Book
from .forms import BookForm
from .utils import searchBooks, paginateBooks
from django.contrib import messages
 

def img_validation(book_data, book,request):
    if not book.image_link:
        try:
            image_list = book_data['items'][0]['volumeInfo']['imageLinks']
            try:
                book.image_link = image_list['thumbnail']
            except KeyError:
                book.image_link = book_data['items'][0]['volumeInfo']['imageLinks']['smallThumbnail']
            except KeyError:
                messages.error(request,"Thumbnail does not exist")
                return HttpResponseRedirect(request.path_info)
        except:
            messages.error(request,"Thumbnail does not exist")
            return HttpResponseRedirect(request.path_info)
    book.save()
    return redirect('books')
values = {0: 'NOT RATED',
        1: 'DO NOT READ',
        2: 'VERY BAD',
        3: 'BAD',
        4: 'MEDIOCRE',
        5: 'SO SO',
        6: 'FINE',
        7: 'GOOD',
        8: 'VERY GOOD',
        9: 'GREAT',
        10:'MASTERWORK'}

def books(request): 
    books, search_query, search_rate, search_order = searchBooks(request)
    custom_range, books, num_pages = paginateBooks(request, books, results=12, interval = 3)
 
    context = {'books': books,
               'search_query': search_query,'ratings': values, 
               'search_rate':search_rate, 'custom_range': custom_range,
               'search_order': search_order, 'num_pages': num_pages}
    return render(request, 'books/books.html',context)
 
def book(request, pk):
    bookObj = Book.objects.get(id=pk)

    context = {'book': bookObj, 'max':range(10)}
    return render(request, 'books/book-review.html', context) 

@login_required(login_url='home')
def createBook(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            
            # ^ add a case when this fail

            try: 
                book_data = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(book.isbn)).json()
                book.title = book_data['items'][0]['volumeInfo']['title']
                authors = book_data['items'][0]['volumeInfo']['authors']
                book.authors = ' - '.join([str(elem) for elem in authors])
                return img_validation(book_data, book,request)
            except:
                book.save()
                return redirect('books')
            
            
    context = {'form': form}
    return render(request, "books/book-form.html", context)

@login_required(login_url="home")
def updateBook(request, pk):
    # profile = request.user.profile
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':

        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            try:
                book_data = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(book.isbn)).json()
                book.title = book_data['items'][0]['volumeInfo']['title']
                authors = book_data['items'][0]['volumeInfo']['authors']
                book.authors = ' - '.join([str(elem) for elem in authors])
                return img_validation(book_data, book,request)
            except:
                book.save()
                return redirect('books')



    context = {'form': form}
    return render(request, "books/book-form.html", context)