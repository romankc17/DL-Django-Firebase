from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, ajax
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    # path('fill_data', views.fill_data, name='fill_data'),
    path('login/',auth_views.LoginView.as_view(template_name='liscence/login.html'), name='login' ),
    path('logout/', auth_views.LogoutView.as_view(template_name='liscence/logout.html'), name='logout'),
    path('clients/', views.list_clients, name='clients'),
    # path('client/<int:pk>', views.ClientDetailView.as_view(), name='client_detail'),
    # path('client/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    # path('client/<int:pk>/success_link', views.success_link, name='success_link'),
    # path('client/<int:pk>/update/', views.ClientUpdateView.as_view(), name = 'client_update' ),

    path('users/create',views.create_user,name='create_user'),
    path('users/',views.list_users,name='list_users'),
    path('clients/filter/',views.clients_filter,name='clients_filter'),

    #ajax
    path('ajax_captcha_entry', ajax.captcha_entry, name='ajax_captcha_entry'),
    path('ajax_submit_captcha', ajax.submit_captcha, name='ajax_submit_captcha'),
    path('delete_client', ajax.delete_client, name='delete_client'),
    path('reset_password', ajax.reset_password, name='reset_password'),
    path('user_update', ajax.user_update, name='user_update'),
    path('user_delete', ajax.user_delete, name='user_delete'),




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)