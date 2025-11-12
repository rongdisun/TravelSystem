from django.urls import path
from . import views

app_name = "travel"

urlpatterns = [
    path('attraction_detail/<int:pk>/', views.AttractionDetailView.as_view(), name='attraction_detail'),
    path('attraction_favorite/<int:pk>/', views.attraction_toggle_favorite, name='attraction_toggle_favorite'),
    path('attraction_visited/<int:pk>/', views.attraction_toggle_visited, name='attraction_toggle_visited'),
    path('tourpackage_detail/<int:pk>/', views.TourPackageDetailView.as_view(), name='tourpackage_detail'),
    path('tourpackage_favorite/<int:pk>/', views.toggle_tour_package_favorite, name='tourpackage_favorite'),
    path('submit_order/<int:pk>/', views.SubmitOrderView.as_view(), name='submit_order'),

    path('', views.AttractionListView.as_view(), name='attraction_list'),
    path('attraction_search/', views.AttractionSearchView.as_view(), name='attraction_search'),
    path('attraction_my_favorite/', views.MyFavoriteAttraction.as_view(), name='attraction_my_favorite'),
    path('attraction_my_visited/', views.MyVisitedAttraction.as_view(), name='attraction_my_visited'),

    path('tour_package_list/', views.TourPackageListView.as_view(), name='tour_package_list'),
    path('tour_package_search/', views.TourPackageSearchView.as_view(), name='tour_package_search'),
    path('tour_package_my_favorite/', views.MyFavoriteTourPackage.as_view(), name='tour_package_my_favorite'),
    path('my_order/', views.MyOrderView.as_view(), name='my_order'),
]
