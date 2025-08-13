from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests', views.viewsets_guest )
router.register('rezervations', views.viewsets_reservation )
router.register('movies', views.viewsets_movie )

urlpatterns = [
    path('admin/', admin.site.urls),


    # 2
    path('django/jsonresponsefrommodel', views.no_rest_from_model),

    # 3.1 GET POST
    path('rest/fbv/', views.FBV_List),

    # 3.2 GET PUT DELETE
    path('rest/fbv/<int:pk>/', views.FBV_pk),

    # 4.1 GET POST from rest freamework class based views APIView
    path('rest/cbv/', views.CBV_List.as_view()),

    # 4.2 GET PUT and DELETE from rest freamework class based views APIView
    path('rest/cbv/<int:pk>/', views.CBV_pk.as_view()),

    # 5.1 GET POST from rest freamework class based views Mixins
    path('rest/mixins/', views.mixins_list.as_view()),

    # 5.2 GET PUT and DELETE from rest freamework class based views Mixins
    path('rest/mixins/<int:pk>/', views.mixins_pk.as_view()),

    # 6.1 GET POST from rest freamework class based views Generics
    path('rest/generics/', views.generics_list.as_view()),

    # 6.2 GET PUT and DELETE from rest freamework class based views Generics
    path('rest/generics/<int:pk>/', views.generics_pk.as_view()),

    # 7 Viewsets
    path('rest/viewsets/', include(router.urls)),

    # 8 Find movie
    path('fbv/findmovie/', views.find_movie),

    # 9 create new reservation
    path('fbv/newreservation/', views.create_new_reservation),

    # 10 rest auth user
    path('api-auth', include('rest_framework.urls')),

    # 11 token authentication
    path('api-token-auth', obtain_auth_token),

    # 12 Post_pk generics
    # path('post/generics/', views.generics_list()),
    path('post/generics/<int:pk>/', views.Post_pk.as_view()),

]
