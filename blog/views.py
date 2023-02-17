from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog

class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview', 'created_user')
    success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_user = self.request.user
            self.object.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview')
    success_url = reverse_lazy('blog:blog')


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog')


class BlogDetailView(DetailView):
    model = Blog

    def get(self, request, pk):
        item = get_object_or_404(Blog, pk=pk)
        item.views_num += 1
        item.save()
        return super().get(self, request, pk)
