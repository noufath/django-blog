from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, PostForm
from django.db.models import Q
from django.views.generic import CreateView
from allauth.account.views import LoginView, LogoutView, SignupView


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_result.html', context)


def index(request):
    queryset = Post.objects.all()
    categories = Category.objects.all()
    # view paginator 2 block
    paginator = Paginator(queryset, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var
    }
    return render(request, 'index.html', context)


def blog(request, blog_id):
    blog = get_object_or_404(Post, id=blog_id)
    categories = Category.objects.all()
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = blog
            form.save()
            return redirect('blog', blog_id=blog_id)

    content = {
        'blog': blog,
        'categories': categories,
        'form': form
    }
    return render(request, 'blog.html', content)


def CategoryView(request, cats):
    category_post = Post.objects.filter(categories__title__contains=cats)
    category_selected = Category.objects.exclude(title__contains=cats)
    context = {
        'cats': cats,
        'category_post': category_post,
        'cat_selected': category_selected
    }
    return render(request, 'categories.html', context)


def blog_create(request):
    title = 'create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('blog', kwargs={
                'blog_id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)


def blog_update(request, blog_id):
    title = 'Update'
    blog = get_object_or_404(Post, id=blog_id)
    form = PostForm(request.POST or None,
                    request.FILES or None,
                    instance=blog
                    )
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('blog', kwargs={
                'blog_id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)


def blog_delete(request, blog_id):
    blog = get_object_or_404(Post, id=blog_id)
    blog.delete()
    return redirect('index')


class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'


class AccountSignUpView(SignupView):
    # Signup View Extended
    template_name = "signup.html"


account_signup_view = AccountSignUpView.as_view()


class AccountLoginView(LoginView):
    # Login View Extended
    template_name = "login.html"


account_login_view = AccountLoginView.as_view()


class AccountLogoutView(LogoutView):
    # Logout Extended
    template_name = "logout.html"


account_logout_view = AccountLogoutView.as_view()
