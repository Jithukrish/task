from django.urls import path
from . views import AcceptedApplicationsCountView, AcceptedApplicationsView, AppliedJobSeekersListView, CreateJobPostView,AddEducationView, JobAppliListview, JobApplicationCountView, JobPostCountRecivedView, JobPostCountView, JobseekerReportsView, PendingApplicationsCountView, PendingApplicationsView, RecentAppliedJobsListView, RejectedApplicationsCountView, RejectedApplicationsView, ReportsView, ReportsstatusView, SearchAppliedJobs, SearchManageView, SearchStatusListview, SekkerSearchAllJobsView, TotalCountJobView, TotalCountView
from .import views

urlpatterns = [
    path('create_job_post/', CreateJobPostView.as_view(), name='create_job_post'),
    path('add_education', AddEducationView.as_view(),name="add_education"),
    path('add_salary_range/', views.AddSalaryView.as_view(), name='add_salary_range'),
    path('add_skill/', views.AddSkillView.as_view(), name='add_skill'),

    path('update_job_post/<int:id>/',views.UpdateJobView.as_view(),name="update_job_post"),
    path('job_details/<int:id>/',views.JobDetailsView.as_view(),name="job_details"),
    path('manage_jobs/',views.ManageJobsView.as_view(),name="manage_jobs"),
    path('seeker_view_all_jobs',views.AllJobSeekerView.as_view(),name="seeker_view_all_jobs"),
    path('update_jobs/<int:pk>/',views.UpdateJobPostView.as_view(),name="update_jobs"),
    path('delete_job/<int:pk>/',views.DeleteJobView.as_view(),name="delete_job"),
    path('search_results',views.SearchAllJobsView.as_view(),name="search_results"),#All job se4rach
    path('job_application_list_stat',views.JobApplicationListView.as_view(),name="job_application_list_stat"),
    path('search_results_managejobs',views.SearchResultManagejobsView.as_view(),name="search_results_managejobs"),
    path('search_results_applica',views.SearchResultApplicationView.as_view(),name="search_results_applica"),
    path('applied_job',views.AppliedJobView.as_view(),name="applied_job"),
    # path('jobPapplyseeker/<int:pk>/',views.JobApplyView.as_view(),name="jobPapplyseeker"),
    path('job_apply_seeker/<int:id>/',views.JobApplyView.as_view(),name="job_apply_seeker"),
    path('seeker_viewmore/<int:id>/',views.SeekViewMoreView.as_view(),name="seeker_viewmore"),
    path('job_application/<int:id>/',views.JobApplicationView.as_view(),name="job_application"),
    # path('job_application/<int:id>/',views.job_application,name="job_application"),
    path('status_track_seeker',views.StatusTarckSeekerView.as_view(),name="status_track_seeker"),
    # path('job_application_list_stat',views.JobApplicationListStatView.as_view(),name="job_application_list_stat"),
    path('status_track_update_emp/<int:pk>/',views.StatusTrackUpdateEmpView.as_view(),name="status_track_update_emp"),
    path('job_application_list_stats',views.JobApplicationListStatView.as_view(),name="job_application_list_stats"),
    path('all_applications/<int:pk>/',views.AllApplicationsView.as_view(),name="all_applications"),
    path('download_resume/<int:file>/', views.DownloadResumeView.as_view(), name='download_resume'),
    path('search_results_resume_down',views.SearchResultsResumeDownloadView.as_view(),name="search_results_resume_down"),
    # path('count_total_application',views.JobPostCountsView.as_view(),name="count_total_application"),
    # path('count_total_application1',views.AllJobsCountView.as_view(),name="count_total_application1"),
    path('total_jobs/', JobApplicationCountView.as_view(), name='total_jobs'),
    path('applied_job_user/', JobAppliListview.as_view(), name='applied_job_user'),
    path('accepted_job_user/', AcceptedApplicationsView.as_view(), name='accepted_job_user'),
    path('rejected_job_user/', RejectedApplicationsView.as_view(), name='rejected_job_user'),
    path('pending_job_user/', PendingApplicationsView.as_view(), name='pending_job_user'),
    path('reports/', ReportsView.as_view(), name='reports'),
    path('reports_job/', JobseekerReportsView.as_view(), name='reports_job'),
    path('recent_applied_jobs/', RecentAppliedJobsListView.as_view(), name='recent_applied_jobs'),   
    path('count_total_post/',JobPostCountView.as_view(),name="count_total_post"),
    path('total_count/',TotalCountView.as_view(),name="total_count"),
    path('total_count_c/',TotalCountJobView.as_view(),name="total_count_c"),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # path('get-job-application-counts/', GetJobApplicationCounts.as_view(), name='get_job_application_counts'),

    path('count_total_applied/',JobPostCountRecivedView.as_view(),name="count_total_applied"),
    path('count_total/',AcceptedApplicationsCountView.as_view(),name="count_total"),
    path('count_rejected/',RejectedApplicationsCountView.as_view(),name="count_rejected"),
    path('count_pending/',PendingApplicationsCountView.as_view(),name="count_pending"),
    path('report_view/',ReportsstatusView.as_view(),name="report_view"),
    path('recent_apply/',AppliedJobSeekersListView.as_view(),name="recent_apply"),
    path('search_result/',SearchStatusListview.as_view(),name="search_result"),
    path('search_all_job/',SekkerSearchAllJobsView.as_view(),name="search_all_job"),
    path('applied_job_see/',SearchAppliedJobs.as_view(),name="applied_job_see"),
    path('search_manage/',SearchManageView.as_view(),name="search_manage"),
    # path('send_message/',SendMessageView.as_view(),name="send_message"),
    path('send_message/',views.send_message,name="send_message"),
    path('MailBox/',views.MailBox,name="MailBox"),

    path('MailBoxid/<int:pk>',views.MailBoxid,name="MailBoxid"),
 
  




    # path('seeker_viewmore/<int:id>/',views.seeker_viewmore,name="seeker_viewmore"),
    # path('applied_job',views.applied_job,name="applied_job"),
    # path('jobPapplyseeker/<int:id>/',views.jobPapplyseeker,name="jobPapplyseeker"),
    # path('job_application/<int:id>/',views.job_application,name="job_application"),
    # path('all_applications/<int:id>/',views.all_applications,name="all_applications"),
    # path('download_resume/<int:file>/', views.download_resume, name='download_resume'),
    # path('search_results_resume_down',views.search_results_resume_down,name="search_results_resume_down"),
    # path('job_application_list_stat',views.job_application_list_stat,name="job_application_list_stat"),

    # path('create_job_post',views.create_job_post,name="create_job_post"),
    # path('update_job_post/<int:id>/',views.update_job_post,name="update_job_post"),
    # path('job_details/<int:id>/',views.job_details,name="job_details"),

    # #seeker view all active jobs
    # path('seeker_view_all_jobs',views.seeker_view_all_jobs,name="seeker_view_all_jobs"),
    # path('seeker_viewmore/<int:id>/',views.seeker_viewmore,name="seeker_viewmore"),
    # #seeker view all applied  jobs
    # path('applied_job',views.applied_job,name="applied_job"),

    # path('jobPapplyseeker/<int:id>/',views.jobPapplyseeker,name="jobPapplyseeker"),
    # path('job_application/<int:id>/',views.job_application,name="job_application"),
    # path('update_jobs/<int:id>/',views.update_jobs,name="update_jobs"),
    


    #search jobs seeker
    # path('search_results',views.search_results,name="search_results"),
    #search applica view  employer
    # path('search_results_applica',views.search_results_applica,name="search_results_applica"),
    # path('status_track_seeker',views.status_track_seeker,name="status_track_seeker"),
    # path('job_application_list_stats',views.job_application_list_stats,name="job_application_list_stats"),
    # path('status_track_update_emp/<int:id>/',views.status_track_update_emp,name="status_track_update_emp"),


#employer manage jobs and job seeker
    # path('manage_jobs',views.manage_jobs,name="manage_jobs"),
    # path('delete_job/<int:id>/',views.delete_job,name="delete_job"),
    # path('all_applications/<int:id>/',views.all_applications,name="all_applications"),
    # path('download_resume/<int:file>/', views.download_resume, name='download_resume'),
    # path('search_results_resume_down',views.search_results_resume_down,name="search_results_resume_down"),
    # path('search_results_managejobs',views.search_results_managejobs,name="search_results_managejobs"),
    # path('job_application_list_stat',views.job_application_list_stat,name="job_application_list_stat"),


    
]
