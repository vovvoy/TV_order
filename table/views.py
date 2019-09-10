import datetime

from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, ListView
from .forms import CreateField
from .filters import OrderFilter
from .models import Post, Choice
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
import csv
import xlwt
from django.http import HttpResponse


# class SubPostListView(LoginRequiredMixin, ListView):
#     queryset = Post.objects.all()
#     template_name = 'post_list.html'
#     context_object_name = 'articles'
#
#     def get_queryset(self):
#         articles = Post.objects.all()
#         paginator = Paginator(articles, 14)
#         page = self.request.GET.get('page')
#         try:
#             articles = paginator.page(page)
#         except PageNotAnInteger:
#             articles = paginator.page(1)
#         except EmptyPage:
#             articles = paginator.page(paginator.num_pages)
#         return articles


class SubPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        articles = super().get_queryset()
        # paginator = Paginator(articles, 14)
        # page = self.request.GET.get('page')
        # try:
        #     articles = paginator.page(page)
        # except PageNotAnInteger:
        #     articles = paginator.page(1)
        # except EmptyPage:
        #     articles = paginator.page(paginator.num_pages)
        if self.request.user.is_superuser:
            return articles

        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SubAgent(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'main.html'
    fields = ['choice', 'text', 'post_dates']
    success_url = '/'


def test(request):
    test_create = Post.objects.order_by('id')
    form = CreateField()
    context = {'test_create': test_create, 'form': form}
    return render(request, 'test.html', context)


def addTodo(request):
    form = CreateField
    if request.method == 'POST':
        form = CreateField(request.POST)
        if form.is_valid():
            a = request.POST['date']
            c = request.POST['text']
            b = request.POST['choice']
            author1 = request.user
            post = Post.objects.create(
                post_dates=a, text=c, choice=Choice.objects.get(pk=b), author=author1
            )
            post.save()
            # return render(request, 'test.html', {'form': post})
            return redirect('post_list')
        else:
            print('ERROR')
    return render(request, 'main.html', {'form': form})


def completeTodo(request, todo_id):
    todo = Post.objects.get(pk=todo_id)
    if todo.complete == False:
        todo.complete = True
    else:
        todo.complete = False
    todo.save()
    return redirect('post_list')


def deleteCompleted(request):
    Post.objects.filter(complete__exact=True).delete()
    return redirect('post_list')


def deleteAll(request):
    Post.objects.all().delete()
    return redirect('post_list')


def changeStatus(request, todo_id):
    todo = Post.objects.get(pk=todo_id)
    if todo.reception == False:
        todo.reception = True
    todo.save()
    return redirect('post_list')


def export_users_csv(request):
    today = datetime.date.today()
    to_str = str(today + datetime.timedelta(days=1))
    finish = to_str[8:10] + '.' + to_str[5:7] + '.' + to_str[0:4]
    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = f'attachment; filename="{finish}.txt"'

    writer = csv.writer(response)


    posts = Post.objects.filter(post_dates__contains=finish).values_list('text',)
    for post in posts:
        writer.writerow(post)

    return response


