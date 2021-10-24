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
    path('sl/<str:client_id>/', views.success_link, name='success_link'),
    path('sl/<str:mobile>/<str:ref>/', views.success_link2, name='success_link2'),

    # path('client/<int:pk>/update/', views.ClientUpdateView.as_view(), name = 'client_update' ),

    path('users/create',views.create_user,name='create_user'),
    path('users/',views.list_users,name='list_users'),
    path('clients/filter/',views.clients_filter,name='clients_filter'),
    path('clients/add/newlicense',views.add_clients,name='add_clients'),
    path('clients/add/addcategory/',views.add_category,name='add_category'),

    #ajax
    path('ajax_captcha_entry', ajax.captcha_entry, name='ajax_captcha_entry'),
    path('ajax_submit_captcha', ajax.submit_captcha, name='ajax_submit_captcha'),
    path('delete_client', ajax.delete_client, name='delete_client'),
    path('reset_password', ajax.reset_password, name='reset_password'),
    path('user_update', ajax.user_update, name='user_update'),
    path('client_update', ajax.client_update, name='client_update'),
    path('user_delete', ajax.user_delete, name='user_delete'),
    path('subUpdate', ajax.subUpdate, name='subUpdate'),
    path('mobileUpdate', ajax.mobileUpdate, name='mobileUpdate'),
    path('allowUpdate', ajax.allowUpdate, name='allowUpdate'),
    path('edit_entryUsers', ajax.edit_entryUsers, name='edit_entryUsers'),
    path('get_clients/', ajax.get_clients, name='get_clients'),
    path('search_clients/',ajax.search_clients,name='search_clients'),




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)