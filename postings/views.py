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

        if form.isvalid():
            posting = form.save()
            return redirect('postings:index')

        else:
            context = {
                'form': form
            }
            return render(request, 'create.html', context)


    
    else:
        form = PostForm()

        context = {
            'form': form
        }
        return render(request, 'create.html', context)