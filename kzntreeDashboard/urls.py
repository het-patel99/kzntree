from django.urls import path
from .views import user_login, user_register, user_logout, home, add_category, add_item, build_dashboard, add_build, item_detail, build_detail, home_api, build_dashboard_api

urlpatterns = [
    path('register/', user_register, name='register'),
    path('/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/', home, name='home'),
    path('add_item/', add_item, name='add_item'),
    path('add_category/', add_category, name='add_category'),
    path('build_dashboard/', build_dashboard, name='build_dashboard'),
    path('add_build/', add_build, name='add_build'),
    path('item_detail/<int:item_id>/', item_detail, name='item_detail'),
    path('build_detail/<int:build_id>/', build_detail, name='build_detail'),
    path('api/home/', home_api, name='home_api'),
    path('api/build_dashboard/', build_dashboard_api, name='build_dashboard_api'),
]