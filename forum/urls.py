from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'forum'


urlpatterns = [
    url(r'^$', login_required(views.index), name='forum-index'),
    url(r'^(?P<forum_id>[0-9]+)/$', login_required(views.forum), name='forum-detail'),

    url(r'^topic/(\d+)/$', login_required(views.TopicView.as_view()), name='topic-detail'),
    url(r'^newtopic/(\d+)/$', login_required(views.new_topic), name='new-topic'),
    url(r'^updatetopic/(?P<topic_id>[0-9]+)/$', login_required(views.update_topic), name='update'),
    url(r'^archivetopic/(?P<topic_id>[0-9]+)/$', login_required(views.archive_topic), name='archive'),

    url(r'^updatepost/(?P<topic_id>[0-9]+)/(?P<post_id>[0-9]+)', login_required(views.update_post), name='updatepost'),
    url(r'^deletetopic/(?P<forum_id>[0-9]+)/(?P<topic_id>[0-9]+)/$', login_required(views.delete_topic), name='delete'),
    url(r'^deletepost/(?P<topic_id>[0-9]+)/(?P<post_id>[0-9]+)', login_required(views.delete_post), name='deletepost'),
]
