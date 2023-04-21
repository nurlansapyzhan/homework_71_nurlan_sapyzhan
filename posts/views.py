from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import CreateView, ListView

from posts.forms import SearchForm, CommentPostForm
from posts.models import Post, Comment

User = get_user_model()


class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            self.form = self.get_search_form()
            self.search_value = self.get_search_value()
            return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(username__icontains=self.search_value) | Q(email__icontains=self.search_value) | Q(
                first_name__icontains=self.search_value) | Q(last_name__icontains=self.search_value)
            user = User.objects.filter(query).first()
            if user:
                queryset = queryset.filter(author=user)
            else:
                queryset = queryset.none()
        else:
            subscriptions = self.request.user.subscribers.all()
            queryset = queryset.filter(author__in=subscriptions)
        return queryset.order_by('-created_at')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        for post in context['posts']:
            post.like_count = post.user_likes.count()
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class AddPostView(CreateView):
    model = Post
    fields = ['description', 'image']
    template_name = 'add_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


class CreateCommentView(View):

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        like_count = post.user_likes.count()
        form = CommentPostForm()
        comments = Comment.objects.filter(post=post).order_by('pk')
        context = {'post': post, 'form': form, 'comments': comments, 'like_count': like_count}
        return render(request, 'post_detail.html', context)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            post.save()
            return redirect('index')
        comments = Comment.objects.filter(post=post)
        context = {'post': post, 'form': form, 'comments': comments}
        return render(request, 'post_detail.html', context)


class LikePostView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if user in post.user_likes.all():
            post.user_likes.remove(user)
            post.save()
        else:
            post.user_likes.add(user)
            post.save()
        return redirect('index')
