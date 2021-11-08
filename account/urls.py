from django.contrib.auth import views
from django.urls import path
from .views import wallet, settings, profile, trade

app_name = 'account'
urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('wallet/', wallet, name='wallet'),
	path('settings/', settings, name='settings'),
	path('profile/', profile, name='profile'),
	path('trade/', trade, name='trade'),
]


# urlpatterns = [
#     path('logout/', views.LogoutView.as_view(), name='logout'),

#     path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
#     path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

#     path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# ]