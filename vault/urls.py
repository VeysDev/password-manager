from django.urls import path
from . import views

urlpatterns = [
    path('', views.vault_auth, name='vault-page'),
    path('addGoldbar/', views.addGoldbar, name='add-goldbar' ),
    path('deleteGoldbar/<int:goldbar_id>/', views.deleteGoldbar)
    # path('main/', ) actual page with goldbars
]