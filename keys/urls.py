import debug_toolbar

from django.urls import path, include

from django.shortcuts import redirect

from . import views

app_name = 'keys' # Namespace: keys:detail, keys:index

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('keys/', views.KeyList.as_view(), name='key-list'),
    path('keys/search', views.KeySearchResults.as_view(), name='key-search-results'),
    path('key/<str:pk>', views.KeyDetail.as_view(), name='key-detail'),
    path('key/<str:pk>/lost', views.KeyLost.as_view(), name='key-lost'),
    path('key/<str:pk>/found', views.KeyFound.as_view(), name='key-found'),


    path('people/', views.PersonList.as_view(), name='person-list'),
    path('people/groups', views.PersonListGroup.as_view(), name='person-list-group'),
    path('people/search', views.PersonSearchResults.as_view(), name='person-search-results'),
    path('person/add', views.PersonCreate.as_view(), name='person-add'),
    path('person/<str:pk>', views.PersonDetail.as_view(), name='person-detail'),
    path('person/<str:pk>/update', views.PersonUpdate.as_view(), name='person-update'),
    path('person/<str:pk>/deposit/create', views.DepositCreate.as_view(), name='deposit-create'),
    path('person/<str:pk_p>/deposit/<str:pk_d>', views.DepositDetail.as_view(), name='deposit-detail'),
    path('person/<str:pk_p>/deposit/<str:pk_d>/retain', views.DepositRetain.as_view(), name='deposit-retain'),
    path('person/<str:pk_p>/deposit/<str:pk_d>/return', views.DepositReturn.as_view(), name='deposit-return'),
    path('person/<str:pk_p>/deposit/<str:pk_d>/delete', views.DepositDelete.as_view(), name='deposit-delete'),

    path('rooms/', lambda r: redirect('keys:room-list-building'), name='room-list'),
    path('rooms/building', views.RoomListBuilding.as_view(), name='room-list-building'),
    path('rooms/groups', views.RoomListGroup.as_view(), name='room-list-group'),
    path('rooms/search', views.RoomSearchResults.as_view(), name='room-search-results'),
    path('room/<slug:slug>', views.RoomDetail.as_view(), name='room-detail'),

    path('issues', lambda r: redirect('keys:issue-list-active'), name='issue-list'),
    path('issues/active', views.IssueListActive.as_view(), name='issue-list-active'),
    path('issues/all', views.IssueListAll.as_view(), name='issue-list-all'),
    path('issues/search', views.IssueSearchResults.as_view(), name='issue-search-results'),
    path('issue/new', views.IssueNew.as_view(), name='issue-new'),
    path('issue/<str:pk>', views.IssueDetail.as_view(), name='issue-detail'),
    path('issue/<str:pk>/return', views.IssueReturn.as_view(), name='issue-return'),

]
