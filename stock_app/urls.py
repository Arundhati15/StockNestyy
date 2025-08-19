from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Pages
    path('', views.index, name='home'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add/', views.add_stock, name='add_stock'),
    path('edit/<int:pk>/', views.edit_stock, name='edit_stock'),
    path('delete/<int:pk>/', views.delete_stock, name='delete_stock'),
    path("get_stock_data/", views.get_stock_data, name="get_stock_data"),
    path("quick_quote/", views.quick_quote, name="quick_quote"),

    # Auth
    #path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('signup/', views.signup, name='signup'),
    
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # APIs
    path('stock/<str:symbol>/', views.stock_detail, name='stock_detail'),
    path('get_stock_data/', views.get_stock_data, name='get_stock_data'),  # single symbol (you already added earlier)
    path('api/quotes/', views.api_quotes, name='api_quotes'),             # multi-symbol (for watchlist)
    path('api/history/', views.api_history, name='api_history'),          # for charts
]
