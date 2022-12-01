from django.urls import path
from core.homepage.views.frequent_questions.views import *
from core.homepage.views.mainpage.views import IndexView, TrackOrderView
from core.homepage.views.services.views import *
from core.homepage.views.social_networks.views import *
from core.homepage.views.team.views import *
from core.homepage.views.testimonials.views import *
from core.homepage.views.comments.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('track/order/', TrackOrderView.as_view(), name='track_order'),
    # services
    path('services/', ServicesListView.as_view(), name='services_list'),
    path('services/add/', ServicesCreateView.as_view(), name='services_create'),
    path('services/update/<int:pk>/', ServicesUpdateView.as_view(), name='services_update'),
    path('services/delete/<int:pk>/', ServicesDeleteView.as_view(), name='services_delete'),
    # frequentquestions
    path('frequent/questions/', FrequentQuestionsListView.as_view(), name='frequent_questions_list'),
    path('frequent/questions/add/', FrequentQuestionsCreateView.as_view(), name='frequent_questions_create'),
    path('frequent/questions/update/<int:pk>/', FrequentQuestionsUpdateView.as_view(), name='frequent_questions_update'),
    path('frequent/questions/delete/<int:pk>/', FrequentQuestionsDeleteView.as_view(), name='frequent_questions_delete'),
    # socialnetworks
    path('social/networks/', SocialNetworksListView.as_view(), name='social_networks_list'),
    path('social/networks/add/', SocialNetworksCreateView.as_view(), name='social_networks_create'),
    path('social/networks/update/<int:pk>/', SocialNetworksUpdateView.as_view(), name='social_networks_update'),
    path('social/networks/delete/<int:pk>/', SocialNetworksDeleteView.as_view(), name='social_networks_delete'),
    # testimonials
    path('testimonials/', TestimonialsListView.as_view(), name='testimonials_list'),
    path('testimonials/add/', TestimonialsCreateView.as_view(), name='testimonials_create'),
    path('testimonials/update/<int:pk>/', TestimonialsUpdateView.as_view(), name='testimonials_update'),
    path('testimonials/delete/<int:pk>/', TestimonialsDeleteView.as_view(), name='testimonials_delete'),
    # team
    path('team/', TeamListView.as_view(), name='team_list'),
    path('team/add/', TeamCreateView.as_view(), name='team_create'),
    path('team/update/<int:pk>/', TeamUpdateView.as_view(), name='team_update'),
    path('team/delete/<int:pk>/', TeamDeleteView.as_view(), name='team_delete'),
    # comments
    path('comments/', CommentsListView.as_view(), name='comments_list'),
    path('comments/delete/<int:pk>/', CommentsDeleteView.as_view(), name='comments_delete'),
]
