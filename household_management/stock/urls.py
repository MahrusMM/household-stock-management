from django.contrib import admin
from django.urls import path, include
from stock import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='home'),  # ✅ Redirect '/' to Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view-stock/', views.view_stock, name='view_stock'),
    path('add-stock/', views.add_stock, name='add_stock'),
    path('delete-stock/<int:item_id>/', views.delete_stock, name='delete_stock'),
    path('view-requests/', views.view_requests, name='view_requests'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('request-stock/', views.request_stock, name='request_stock'),
    path('settings/', views.settings_page, name='settings'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
