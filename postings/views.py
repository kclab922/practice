from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    postings = Post.objects.all()

    context = {
        'postings': postings
    }

    return render(request, 'index.html', context)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            posting = form.save()
            return redirect('postings:index')

    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'create.html', context)


def delete(request, id):
    posting = Post.objects.get(id=id)

    posting.delete()

    return redirect('postings:index')


def update(request, id):
    posting = Post.objects.get(id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=posting)

        if form.is_valid():
            form.save()
            return redirect ('postings:index')
    
    else:
        form = PostForm(instance=posting)

    context = {
        'form': form
    }
    
    return render(request, 'update.html', context)


 