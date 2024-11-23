from django.shortcuts import render
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404
from .models import *

from django.core.cache import cache



class PostList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

   # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
     #   context['time_now'] = datetime.utcnow()
      #  context['next_sale'] = "Все свежие новости в эту среду!"
      #  return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context




class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        print('------------')
        print(obj)
        print('------------')
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        print('***************')
        print(obj)
        print('***************')
        return obj




class PostSearch(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 2


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = ('news.add_post')


    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            post.positions = "AR"
        post.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = ('news.change_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/edit/':
            post.positions = "AR"
        post.save()
        return super().form_valid(form)




class PostDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('post_list')


    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/delete/':
            post.positions = "AR"
        post.save()
        return super().form_valid(form)

#from django.views.generic.edit import CreateView

class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )


class ChangePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    # а дальше пишите код вашего представления


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'


    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-create_time')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)


    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


