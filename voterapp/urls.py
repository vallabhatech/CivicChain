from django.urls import path
from . import views as voterViews

urlpatterns = [ 
    path('register/<int:cand_id>',voterViews.voter_register,name='voter_register'),
    path('elections',voterViews.voter_elections,name='voter_elections'),
    path('voter-results',voterViews.voter_results,name='voter_results'),
    path('voting/<int:id>',voterViews.voter_voting_page,name='voter_voting'),
    path('cast-vote/<int:id>/<int:cand_id>',voterViews.cast_vote,name='cast_vote'),
    path('vote-otp/<int:id>/<int:cand_id>',voterViews.voter_otp,name='voter_otp'),
    path('voter-view-result/<int:id>',voterViews.voter_verify_results,name='voter_verify_results')
]