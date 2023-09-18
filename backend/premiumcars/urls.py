from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from rent import views
from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router.urls)),
    path('api/cars/', views.CarView.as_view()),
    path('api/cars/<int:id>', views.CarDetailView.as_view()),
    path('api/brands/<str:brand>/', views.BrandCarsView.as_view()),
    path('api/brands/', views.BrandView.as_view()),
    path('api/car/<int:id>', views.CarDetailView.as_view()),

    path('api/rent/', views.RentalView.as_view()),
    path('api/rent/add', views.RentalCreate.as_view()),
    path('api/rent/<int:pk>', views.RentalDestroyView.as_view()),


    path('api/user/', views.UserView.as_view()),
    path('api/user/password', views.ChangePasswordView.as_view()),

    path('token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),



    path("admin/", admin.site.urls),
    path('', include('rent.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
