import ast
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    JsonResponse)
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.views import get_client_ip
from posts.forms import CommentForm, PostForm
from posts.models import Follow, Ip, Like, Post
from yatube.settings import COUNT_PAGINATOR_PAGE

User = get_user_model()


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = COUNT_PAGINATOR_PAGE

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()

        context["mediaURL"] = settings.MEDIA_URL
        if self.request.user.is_authenticated:
            context["posts_like"] = Post.objects.filter(
                like__user=self.request.user,
                like__like=True)
        return context


class GroupPostView(ListView):
    model = Post
    template_name = 'posts/group_list.html'
    paginate_by = COUNT_PAGINATOR_PAGE

    def get_queryset(self):
        return get_list_or_404(Post, group__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()
        context["mediaURL"] = settings.MEDIA_URL
        if self.request.user.is_authenticated:
            context["posts_like"] = Post.objects.filter(
                like__user=self.request.user,
                like__like=True)
        return context


class ProfileDetailView(ListView):
    model = Post
    paginate_by = COUNT_PAGINATOR_PAGE
    template_name = 'posts/profile.html'

    def get_queryset(self):
        return (
            Post.objects.select_related('author')
            .filter(author__username=self.kwargs['username'])
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()
        context["mediaURL"] = settings.MEDIA_URL
        context["author"] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        if (
            Follow.objects.filter(
                user__username=self.request.user,
                author__username=self.kwargs['username']).exists()
        ):
            context["following"] = True
        return context


class PostDetailView(CreateView):
    form_class = CommentForm
    template_name = 'posts/post_detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()
        context["mediaURL"] = settings.MEDIA_URL
        if self.request.user.is_authenticated:
            context["posts_like"] = Post.objects.filter(
                like__user=self.request.user,
                like__like=True)
        context["post"] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        context["comments"] = context["post"].comment.all()
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        ip = get_client_ip(self.request)
        if Ip.objects.filter(ip=ip).exists():
            post.views.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            post.views.add(Ip.objects.get(ip=ip))
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()
        context["is_edit"] = False
        return context


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        if form.instance.author != self.request.user:
            return HttpResponseForbidden()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_detail', args=[self.kwargs['post_id']])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()
        context["is_edit"] = True
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = None

    def get_success_url(self):
        username = (
            get_object_or_404(Post, pk=self.kwargs['post_id'])
            .author.username
        )
        return reverse('posts:profile', args=[username])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.author == self.request.user:
            self.object.delete()
        return HttpResponseRedirect(success_url)

    def get(self, request, post_id):
        return HttpResponseRedirect(reverse(
            'posts:post_detail',
            args=[post_id])
        )


class CommentCreate(LoginRequiredMixin, CreateView):
    template_name = 'posts/post_detail.html'
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()
        context["mediaURL"] = settings.MEDIA_URL
        context["post"] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        context["comments"] = context["post"].comment.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        self.object.save()
        return super().form_valid(form)


class FollowIndex(LoginRequiredMixin, ListView):
    template_name = 'posts/follow.html'
    paginate_by = COUNT_PAGINATOR_PAGE

    def get_queryset(self):
        posts = Post.objects.filter(
            author__following__user=self.request.user
        )
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()
        context["mediaURL"] = settings.MEDIA_URL
        if self.request.user.is_authenticated:
            context["posts_like"] = Post.objects.filter(
                like__user=self.request.user,
                like__like=True)
        return context


class ProfileFollow(LoginRequiredMixin, UpdateView):
    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        follow_create = Follow.objects.filter(
            user=request.user, author=author
        ).exists()
        if not follow_create and author != request.user:
            Follow.objects.create(user=request.user, author=author)
        return HttpResponseRedirect(reverse('posts:follow_index'))


class ProfileUnfollow(LoginRequiredMixin, UpdateView):
    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        follow_delet = get_object_or_404(
            Follow,
            user=request.user, author=author
        )
        if follow_delet:
            follow_delet.delete()
        return HttpResponseRedirect(reverse('posts:follow_index'))


class PostLike(UpdateView):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return JsonResponse({'result': 404})
        data = ast.literal_eval(request.GET['data'] or None)
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        if Like.objects.filter(user=self.request.user, post_like=post).exists():
            obj_like = Like.objects.get(user=self.request.user, post_like=post)
            obj_like.like = not obj_like.like
            obj_like.save()
        else:
            obj_like = Like.objects.create(like=not data, user=self.request.user)
            post.like.add(obj_like)

        return JsonResponse(
            {'result': data, 'like_cout': post.like_count()}
        )


class FavoritViewsView(ListView):
    model = Post
    template_name = 'posts/view_count_list.html'
    paginate_by = COUNT_PAGINATOR_PAGE

    def get_queryset(self):
        return Post.objects.annotate(total=Count('views')).order_by('-total')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(created__icontains=datetime.date.today()).count()
        context["mediaURL"] = settings.MEDIA_URL
        if self.request.user.is_authenticated:
            context["posts_like"] = Post.objects.filter(
                like__user=self.request.user,
                like__like=True)
        return context
