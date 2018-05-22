from django.urls import path
from scheduling import views

app_name = 'scheduling'

urlpatterns = [
    # /scheduling/
    path('', views.scheduling, name='scheduling'),
    
    #### DOCENTS ####

    # scheduling/docent
    path('docent', views.DocentIndex.as_view(), name='doc_index'),
    # scheduling/docent/name
    path('docent/<slug:slug>/', views.DocentDetail.as_view(), name='doc_detail'),
    # scheduling/docent/create
    path('docent/create', views.DocentCreate.as_view(), name='doc_create'),
    # scheduling/docent/name/update
    path('docent/<str:name>/update', views.DocentUpdate.as_view(), name='doc_update'),
    # scheduling/docent/name/delete
    path('docent/<str:name>/delete', views.DocentDelete.as_view(), name='doc_delete'),

    
    #### REQUESTS #####
    # scheduling/request-list/
    path('request-list', views.RequestIndex.as_view(), name='req_index'),
    # scheduling/request/entry
    path('request/entry', views.RequestCreate.as_view(), name='req_entry'),
    # scheduling/request/#
    path('request/<int:pk>', views.RequestUpdate.as_view(), name='req_update'),
    # scheduling/request/#/delete
    path('request/<int:pk>/delete', views.RequestDelete.as_view(), name='req_delete'),

    #### RESERVATIONS ####

    # scheduling/reservation
    path('reservation', views.ReservationIndex.as_view(), name='res_index'),
    # scheduling/reservation/detail/#
    path('reservation/<int:pk>/detail', views.ReservationDetail.as_view(), name='res_detail'),
    # scheduling/reservation/create
    path('reservation/create', views.ReservationCreate.as_view(), name='res_create'),
    # scheduling/reservation/create-from-request/#
    path('reservation/create-from-request/<int:pk>', views.ReservationCreateFromRequest.as_view(),
         name='res_create_from_req'),
    # scheduling/reservation/#
    path('reservation/<int:pk>', views.ReservationUpdate.as_view(), name='res_update'),
    # scheduling/reservation/#/delete
    path('reservation/<int:pk>/delete', views.ReservationDelete.as_view(), name='res_delete'),

    #### CUSTOMER PROFILES ####

    # scheduling/profiles
    path('profiles', views.CustomerProfileIndex.as_view(), name='prof_index'),
    # scheduling/profiles/name
    path('profiles/<slug:slug>/', views.CustomerProfileDetail.as_view(), name='prof_detail'),
    # scheduling/profiles/create
    path('profiles/create', views.CustomerProfileCreate.as_view(), name='prof_create'),
    # scheduling/profiles/create-from-request
    path('profiles/create-from-request/<int:pk>', views.CustomerProfileCreateFromRequest.as_view(),
         name='prof_create_from_req'),
    # scheduling/profiles/name/update
    path('profiles/<str:name>/update', views.CustomerProfileUpdate.as_view(), name='prof_update'),
    # scheduling/profiles/name/delete
    path('profiles/<str:name>/delete', views.CustomerProfileDelete.as_view(), name='prof_delete'),

    #### Statistics ####
    path('statistics/', views.statistics.as_view(), name='statistics'),
    ]
