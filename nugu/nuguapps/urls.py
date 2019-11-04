from django.urls import path
from . import views
app_name = 'nugu'

urlpatterns = [
    # path('timer', views.timer, name='timer'),
    path('check_schedule', views.check_schedule, name='schedule'),
    # path('subject', views.subject, name='subject'),

    path('', views.index, name='index'),
    
    # path('ask_result', views.ask_result),
    path('year_ko_ab', views.year_ko_ab),
    path('infom_other_information', views.infom_other_information, name='infom_other_information'),
    path('inform_univ_information', views.inform_univ_information, name='inform_univ_information'),
    path('inform_univ_my', views.inform_univ_my, name='inform_univ_my'),
    path('answer_univ_other', views.answer_univ_other, name='answer_univ_other'),
    
    
    
    path('ask_read', views.ask_read, name = 'ask_read'),
    path('schedule.upgrade.content', views.schedule_upgrade_content),
    path('edit_content', views.edit_content, name='edit_content'),
    path('delete_finish',views.delete_finish, name='delete_finish'),
    
    
    path('answer_subject_num',views.answer_subject_num),
    path('check_no_num', views.check_no_num),
    
    # path('answer_grade_result',views.answer_grade_result),
    path('compare_with_other', views.compare_with_other),
    path('compare_with_goal', views.compare_with_goal),
    path('health', views.health),
    path('condition_insomnia', views.condition_insomnia),
    path('condition_stress', views.condition_stress),
    path('condition_concentration', views.condition_concentration),
]
