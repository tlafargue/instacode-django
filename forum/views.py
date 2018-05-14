from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.template.context_processors import csrf
from .models import Forum, Topic, Post
from .forms import TopicForm, PostForm, UpdateTopicForm
from .settings import *
from django.views.generic import TemplateView,FormView
from django.db.models import Q
from django.contrib.auth.models import User





def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

def archive_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    user = request.user
    if (user.is_superuser):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                forum = Forum.objects.get(title='archive')
                Topic.objects.filter(pk=topic_id).update(forum=forum.id,closed=True)
                return redirect('forum:topic-detail', topic.id)
        return render(request, 'forum/archiveform.html')
    return redirect('forum:topic-detail', topic.id)


def delete_post(request, topic_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    topic = get_object_or_404(Topic, pk=topic_id)
    user = request.user
    if ((user.id == post.creator.id and topic.closed==False) or user.is_superuser):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post.delete()
                return redirect('forum:topic-detail', topic_id)
        return render(request, 'forum/deleteform.html')
    return redirect('forum:topic-detail', topic_id)


def delete_topic(request, forum_id ,topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    user = request.user
    if (user.id == topic.creator.id and topic.closed==False) or user.is_superuser:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                topic.delete()
                return redirect('forum:forum-detail',forum_id)
        return render(request, 'forum/deletetopicform.html')
    return redirect('forum:forum-detail', forum_id)

def forum(request, forum_id):
    """Listing of topics in a forum."""
    topics = Topic.objects.filter(forum=forum_id).order_by("-created")
    topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)
    forum = get_object_or_404(Forum, pk=forum_id)
    user = request.user
    context = {'topics': topics, 'forum': forum, 'user':user}
    return render(request,"forum/forum.html",context)

def index(request):
    """Main listing."""
    forums = Forum.objects.all()
    queryset_list = Topic.objects.all()
    query = request.GET.get("q")
    if query:

        try:
            user = User.objects.get(username=query)
            topic = queryset_list.filter(Q(creator=user.id))
            user = request.user
        except:
            user = request.user
            topic = queryset_list.filter(
                Q(description__icontains=query) |
                Q(title__icontains=query)
            ).distinct()

        context = {'topics': topic, 'user': user}
        return render(request, "forum/forumsearch.html", context)
    else:
        return render(request,"forum/list.html", {'forums': forums,'user': request.user})


def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


def new_topic(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    if (forum.categorie!="Archive"):
        form = TopicForm()
        if request.method == 'POST':
            form = TopicForm(request.POST)
            if form.is_valid():
                topic = Topic()
                topic.title = form.cleaned_data['title']
                topic.description = form.cleaned_data['description']
                topic.forum = forum
                topic.creator = request.user
                topic.save()
                return redirect('forum:topic-detail', topic.id)
        return render(request,'forum/new-topic.html', {
            'form': form,
            'forum': forum,})
    return redirect('forum:forum-detail', forum.id)



class TopicView(FormView):
    template_name = 'forum/topic.html'
    def get(self, request, topic_id):
        form = PostForm()
        posts = Post.objects.filter(topic=topic_id).order_by("created")
        posts = mk_paginator(request, posts, DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE)
        topic = Topic.objects.get(pk=topic_id)
        forum = get_object_or_404(Forum, pk=topic.forum.id)
        user = request.user
        context = {'forum':forum,'form':form,'posts':posts, 'topic':topic, 'user':user}
        return render(request, self.template_name, context)
    def post(self, request, topic_id):
        topic = Topic.objects.get(pk=topic_id)
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.topic = topic
            post.body = form.cleaned_data['body']
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']
            post.save()
            topic = Topic.objects.get(pk=topic_id)
            return redirect('forum:topic-detail', topic.id)
        context = {'topic': topic, 'form': form}
        return render(requesr, self.template_name, context)


def update_post(request, topic_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    topic =get_object_or_404(Topic, pk=topic_id)
    user = request.user
    if (user.id == post.creator.id) and (topic.closed==False):
        form = PostForm()
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                bodyobj = form.cleaned_data['body']
                Post.objects.filter(pk=post_id).update(body=bodyobj)
                return redirect('forum:topic-detail', topic_id)
        return render(request, 'forum/post-form.html', {
            'form': form,
        })
    return redirect('forum:topic-detail', topic_id)



def update_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    user = request.user
    if (user.id == topic.creator.id) and (topic.closed==False):
        form = UpdateTopicForm()
        if request.method == 'POST':
            form = UpdateTopicForm(request.POST)
            if form.is_valid():
                descriptionobj = form.cleaned_data['description']
                Topic.objects.filter(pk=topic_id).update(description=descriptionobj)
                return redirect('forum:topic-detail', topic.id)
        return render(request, 'forum/update-topic.html', {
            'form': form,
        })
    return redirect('forum:topic-detail', topic.id)





