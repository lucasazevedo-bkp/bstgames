from django.urls import path
from .views import (
    HomeView, SignUpView, LogInView, LogOutView, VerifyEmailView, 
    SendVerifyEmailView, PasswordChangeView, PasswordResetView,
    PasswordResetConfirmView, PlatformGameListView, GameDetailView,
    GameSearchListView, GameMarketView, EditProfileView, viacep_ajax,
    market_table_ajax,
)

app_name = 'bstgames'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('send-verify-email/', SendVerifyEmailView.as_view(), name='send-verify-email'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('platform/<int:pk>/games/', PlatformGameListView.as_view(), name='list-platform-games'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='detail-game'),
    path('search-game/', GameSearchListView.as_view(), name='search-game'),
    path('game-maket/<int:pk>/<int:action>/', GameMarketView.as_view(), name='game-maket'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('viacep-ajax/', viacep_ajax, name='viacep-ajax'),
    path('market-table-ajax/', market_table_ajax, name='market-table-ajax'),
]
