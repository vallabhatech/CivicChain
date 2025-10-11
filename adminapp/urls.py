from django.urls import path
from . import views as adminViews

urlpatterns = [ 
            path('login',adminViews.admin_login,name='admin_login'),
            path('dashboard',adminViews.admin_dashboard, name='admin_dashboard'),
            path('add-election',adminViews.admin_add_election,name='admin_add_election'),
            path('add-candidate',adminViews.admin_add_candidates,name='admin_add_candidates'),
            path('results',adminViews.admin_results,name='admin_results'),
            path('view-elections',adminViews.admin_view_elections,name='admin_view_elections'),
            path('view-candidates/<int:id>',adminViews.admin_view_candidates,name='admin_view_candidates'),
            path('verify-results/<int:id>',adminViews.verify_results,name='verify_results')
]