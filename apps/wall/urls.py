from django.conf.urls import url
from . import views   

urlpatterns = [
    url(r'^$', views.signin),
    url(r'^reg_process$', views.reg_process),
    url(r'^log_process$', views.log_process),
    url(r'^clear$', views.clear),
    url(r'^wall$', views.wall),
    url(r'^wall_post$', views.wall_post),
    url(r'^wall_comment/(?P<num>\d+)$', views.wall_comment),
    url(r'^wall_delete/(?P<num>\d+)$', views.wall_delete),
    url(r'^clear_all$', views.clear_all),
]