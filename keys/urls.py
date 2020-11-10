from django.urls import path

from . import views

app_name = 'keys' # Namespace: keys:detail, keys:index

urlpatterns = [
    path('', views.index_view, name='index'),
    path('keys/', views.KeyList.as_view(), name='key-list'),
    path('keys/search', views.KeySearchResults.as_view(), name='key-search-results'),
    path('key/<str:pk>', views.KeyDetail.as_view(), name='key-detail'),

    path('people/', views.PersonList.as_view(), name='person-list'),
    path('people/search', views.PersonSearchResults.as_view(), name='person-search-results'),
    path('person/add', views.PersonCreate.as_view(), name='person-add'),
    path('person/<str:pk>',views.PersonDetail.as_view(), name='person-detail'),

    path('issues', views.IssueList.as_view(), name='issue-list'),
    path('issues/search', views.IssueSearchResults.as_view(), name='issue-search-results'),
    path('issues/return', views.IssueReturnList.as_view(), name='issue-return-list'),
    path('issue/new', views.IssueNew.as_view(), name='issue-new'),
    path('issue/<str:pk>', views.IssueDetail.as_view(), name='issue-detail'),
    path('issue/<str:pk>/return', views.IssueReturn.as_view(), name='issue-return'),

]
