# CRUD
- Create Read Update Delete


## 프로젝트 기본 설정

1. 프로젝트 폴더 생성 및 vscode 열기

2. `.gitignore`, `README.md` 만들기 (추후 돌이키기 어려우므로 미리 생성)

3. django 프로젝트 생성
```
django-admin startproject <pjt-name> .
```

4. 가상환경 설정(생성)
```
python -m venv venv 
# 파이썬 실행 / module 사용할게 / venv: 가상환경 virtual environment / 내가 만들려는 폴더명
```

5. 가상환경 활성화 
- 활성화 후 `venv`가 터미널에 출력 되었는지 확인
```
source venv/Scripts/activate
```

6. 가상환경에 django 설치
```
pip install django
```

7. 서버 실행 확인
- `ctrl+c`로 나오기
```
python manage.py runserver
```



## 앱 생성 및 앱 등록

1. 앱 생성
```
django-admin startapp <app-name>
```

2. 앱 등록 => `<pjt-name>폴더`=> `settings.py`
```
INSTALLED_APPS = [
    ...
    `<app-name>`,
]
```


## base.html 설정
1. `base directory`에 `templates` 폴더 생성
2. 폴더 안에 `base.html` 파일 생성
3. `settings.py`에 설정
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]
```




## Modeling

1. 모델 정의 (`model.py`)  
- 모델명은 기본적으로 단수
```python
class Post(models.Model):
    # Charfield 는 TextField에 비해 짦은 내용
    title = models.CharField(max_length=100)
    content = models.TextField()
```

2. 번역본 생성
- 파이썬 세상에서 SQL 세상으로 이주시키기 위한 준비로 번역본 생성
```
python manage.py makemigrations
```

3. DB에 반영
- 이주시켜!
- 내가 만든 posts가 제대로 포함되어있는지가 중요. 
- 길게 나오는 이유는 장고에 내장된 애들이 같이 이주되어서.
```
python manage.py migrate
```

4. 생성한 모델을 admin에 등록
```python
from django.contrib import admin
from .models import Post
     # . => 현재 나와 같은 폴더 내에 있다는 의미

# Register your models here.

admin.site.register(Post)
```

5. admin 계정 생성
```
python manage.py createsuperuser
```

6. `/admin` 서버 접속
- 등록한 모델이 정상 작동 되는지 확인



## CRUD
> Create, Read, Update, Delete



### 1. Read
    - 데이터베이스에 있는 게시물을 읽는 것
    - 주로 index, detail 페이지로 작성

- `<appname>` 폴더에 `templates` 폴더 생성하고 `index.html` 파일 생성 
```html
{% extends 'base.html' %}

{% block body %}

    <h1>index</h1>

    {% for posting in postings %}
    <p>{{ posting.title }}</p>
    <p>{{ posting.content }}</p>
    <hr>
    {% endfor %}

{% endblock %}
```

- `<pjtname>` 폴더 - `urls.py` (앱으로 연동 설정)
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('postings/', include('postings.urls'))
]
```

- `<appname>` 폴더 - `urls.py`
```python
from django.urls import path
from . import views

app_name = 'postings'

urlpatterns = [
    path('', views.index, name='index'),
]
```

- `<appname>` 폴더 - `views.py`
```python
## index 함수
from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    postings = Post.objects.all()

    context = {
        'postings': postings
    }

    return render(request, 'index.html', context)
```
```python
## detail 함수
def detail(request, id):
    # Post라는 전체데이터에서 get(가져와) 
    # post는 하나의 게시물이므로 단수. 
    post = Post.objects.get(id=id)

    context = {
        'post': post,
    }
    return render(request, 'detail.html', context)
```

- `<appname>/` 서버 정상작동 확인




### 2. Create (ModelForm 활용)
- 사용자에게 데이터 받고, 저장

- `<appname>` - `forms.py` 파일 생성
```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
```

- `create.html` 작성
```python
{% extends 'base.html' %}

{% block body %}

    <form action="" method="POST">
        {% csrf_token %}

        {{ form }}
        
        <input type="submit">
    </form>

{% endblock %}
```

- `url.py`
```python
    path('create/', views.create, name='create'),
```

- `views.py`
```python
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
```

- `base.html` 버튼 만들기
```html
<body>
    <h1>여기는 Base</h1>
    <a href="{% url 'postings:index' %}">Home</a>
    <a href="{% url 'postings:create' %}">Create</a>
    {% block body %}

    {% endblock %}
</body>
```

- `<appname>/` 서버 정상작동 확인



### 3. Delete
- `index.html`에 delete 버튼 생성
```html
    {% for posting in postings %}
    <p>{{ posting.title }}</p>
    <p>{{ posting.content }}</p>
    <a href="{% url 'postings:delete' id=posting.id %}">Delete</a>
    <hr>
    {% endfor %}
```

- `urls.py`
```python
    path('<int:id>/delete/', views.delete, name='delete')
```

- `views.py`
```python
def delete(request, id):
    posting = Post.objects.get(id=id)
    posting.delete()

    return redirect('postings:index')
```




### 4. Update
    - create 로직과 read 로직의 합