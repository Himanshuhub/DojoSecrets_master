from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^index$', views.index, name = 'index'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),

    url(r'^indexWall$', views.indexWall, name = 'indexWall'),
    url(r'^add_poke$', views.add_poke, name = 'add_poke'),
    url(r'^add_poke$', views.add_poke, name = 'add_poke'),
    # url(r'^add_poke2$', views.add_poke2, name = 'add_poke2'),
    # url(r'^most_popular$', views.most_popular, name = 'most_popular'),
    url(r'^logout$', views.logout, name = 'logout'),
    # url(r'^delete_secret$', views.delete_secret, name = 'delete_secret'),
    # url(r'^delete_secret2$', views.delete_secret2, name = 'delete_secret2')

]
