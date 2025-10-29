from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import TaskPredictionViewSet
from .views import (
    personnel_list,
    CompanySignupView,
    assign_task,
    CompanyChangePasswordView,
    ManagerBulkCreateView,
    EmployeeBulkCreateView,
    ManagerCreateView,
    EmployeeCreateView,
    login_user,
    AttendanceUpdateView,
    AttendanceListView,
    mark_attendance,
    get_counts_by_name,
    get_dashboard_counts,
    get_new_hires_count,
    get_employees,
    GetCompanyNameView,
    EmployeeDetailView,
    get_managers,
    ManagerDetailView,
    get_new_managers_count,
    # The new class-based view for today's attendance
    TodayAttendanceListView,
    DateAttendanceListView,
    AttendancePDFExportView,
    PresentCountView,
    LateArrivalsCountView,
    AbsentCountAPIView,
    AttendanceReportsAPIView,
    WeeklyAttendanceSummaryView,
    DailyAttendanceRatioView,
    AssignTaskView,
     DashboardMeasurementsView,
    PunctualityGraphView,
    OvertimeGraphView,
    PunctualityPredictionGraphView,
    RecommendationView,
    LatePredictionAPIView,
    AbsentPredictionAPIView,
    # OvertimePredictionAPIView,
    AttendanceBonusPredictionAPIView,
    TaskStatusSummaryView,
    AssignedTasksView,
    TaskCompletionView,
    TaskCompletionMonthlyAggregationView,
    TaskPredictionViewSet,
    OvertimePredictionAPIView,
    CompanyTodayAttendanceView,
    AttendanceByDateView,
    EmployeeTodayAttendanceView,
    EmployeeAttendanceByDateView,
    EmployeeTasksView,
    TaskUpdateView,
    TaskWithPredictionView,
    BonusPredictionViewML,
    EmployeeListView,
    PersonnelListView,
    TaskDetailView,
    CompanyDetailView,
    EmployeeTaskListView,
    ChangePasswordView,
    CompanyDetail,
    # EmployeeViewSet
    TaskCapacityPredictionView,
    get_user_tasks,
    TaskBonusPredictionAPIView,
    OverallBonusPredictionAPIView,
    EmployeeDetailUpdateView
)
from django.conf.urls import include

router = DefaultRouter()
# This sets up the new API endpoint: /api/tasks-with-predictions/
router.register(r'tasks-with-predictions', TaskPredictionViewSet, basename='task-prediction')



urlpatterns = [
    
    # Company
    path('signup/', CompanySignupView.as_view(), name='company-signup'),
    path('get-company-name/', GetCompanyNameView.as_view(), name='get-company-name'),

    # Manager
    path('managers/bulk-create/', ManagerBulkCreateView.as_view(), name='manager-bulk-create'),
    path('managers/create/', ManagerCreateView.as_view(), name='manager-create'),
    path('employees/<int:employee_id>/', EmployeeDetailUpdateView.as_view(), name='employee-detail-update'),

    # Employee
    path('employees/bulk-create/', EmployeeBulkCreateView.as_view(), name='employee-bulk-create'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/', get_employees, name='employees-list'),
    path('managers/',get_managers,name='manager-list'),
    path('managers-detail/',get_managers,name='get-managers'),
    path('employees-detail/', get_employees, name='get_employees'),
    path('new-hires-count/', get_new_hires_count, name='new_hires_count'),
    path('new-managers-count/',get_new_managers_count,name='new_managers_count'),
    path('employees/<int:employee_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('managers/<int:manager_id>/', ManagerDetailView.as_view(), name='manager-detail'),
    path('attendance/export_pdf/', AttendancePDFExportView.as_view(), name='export-pdf'),

    # The corrected URL for the new view
    path('attendance/today/', TodayAttendanceListView.as_view(), name='today-attendance-list'),
    path('attendance/particular_date/', DateAttendanceListView.as_view(), name='date-attendance-list'),
    path('attendance/present_count/',PresentCountView.as_view(),name='present_count'),
    # Employee/Company login
    path('login/', login_user, name='user-login'),
    path('attendance/late_arrivals_count/', LateArrivalsCountView.as_view(), name='late_arrivals_count'), # Add this new path
    path('attendance/absent_count/', AbsentCountAPIView.as_view(), name='absent-count'),
    path('attendance/reports/', AttendanceReportsAPIView.as_view(), name='attendance-reports'),
    path('attendance/weekly-attendance-summary/', WeeklyAttendanceSummaryView.as_view(), name='weekly-attendance-summary'),
    path("attendance/attendance-ratio/", DailyAttendanceRatioView.as_view(), name="attendance-ratio"),
    path('attendance/export-report/', views.export_weekly_attendance_pdf, name='export_weekly_attendance_pdf'),

    # Attendance
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/update/', AttendanceUpdateView.as_view(), name='attendance-update'),
    path("mark_attendance/", mark_attendance, name="mark_attendance"),
    path("attendance/attendance-ratio/", DailyAttendanceRatioView.as_view(), name="attendance-ratio"),
    path('attendance/daily_ratio/', DailyAttendanceRatioView.as_view(), name='daily_ratio'),
    path('attendance/daily-punctuality-ratio/', views.daily_punctuality_ratio, name='daily_punctuality_ratio'),
    path('assign-task/', assign_task, name='assign-task'),

    # Dashboard Counts
    path("get-counts/", get_dashboard_counts, name='get_dashboard_counts'),
    path('get-counts-by-name/', get_counts_by_name, name='get_counts_by_name'),

    # path('personallist/<int:company_id>/', PersonnelList.as_view(), name='personallist-by-company'),
#  path("personallist/", views.personnel_list, name="personnel_list"),
    path("assign-task/", views.assign_task, name="assign-task"),
    path("task-list/", views.task_list, name="task_list"),
    path("update-task-status/<int:task_id>/", views.update_task_status, name="update_task_status"),
path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    
    # URL for retrieving, updating, and deleting a single task
    # The <int:pk> part captures the task's ID from the URL (e.g., 9)
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/dashboard-data/', views.task_dashboard_data, name='task_dashboard_data'),
path('dashboard/measurements/<int:company_id>/', DashboardMeasurementsView.as_view(), name='dashboard-measurements'),
    path('dashboard/punctuality/<int:company_id>/', PunctualityGraphView.as_view(), name='punctuality-graph'),
    path('dashboard/overtime/<int:company_id>/', OvertimeGraphView.as_view(), name='overtime-graph'),
    path('dashboard/punctuality/prediction/<int:company_id>/', PunctualityPredictionGraphView.as_view(), name='punctuality-prediction'),
    path('dashboard/recommendations/<int:company_id>/', RecommendationView.as_view(), name='recommendation-list'),
    path('dashboard/punctuality_prediction/<int:company_id>/', PunctualityPredictionGraphView.as_view(), name='punctuality-prediction-api'),
  path('dashboard/late_prediction/<int:companyId>/', LatePredictionAPIView.as_view(), name='late_prediction_api'),
    path('dashboard/absent_prediction/<int:companyId>/', AbsentPredictionAPIView.as_view(), name='absent_prediction_api'),
    path('dashboard/overtime_prediction/<int:companyId>/', OvertimePredictionAPIView.as_view(), name='overtime_prediction_api'),
    path('dashboard/tasks-with-predictions/', TaskWithPredictionView.as_view(), name='tasks-with-predictions'),
   path(
        'api/task/predict/bonus/ml/<str:user_type>/<int:user_id>/', 
        BonusPredictionViewML.as_view(), 
        name='bonus-prediction-ml'
    ),
    
    # .

    # path('dashboard/overtime_prediction/<int:companyId>/', OvertimePredictionAPIView.as_view(), name='overtime_prediction_api'),
    path('dashboard/bonus-prediction/<int:company_id>/', AttendanceBonusPredictionAPIView.as_view(), name='bonus-prediction'),

        path('tasks/status-summary/', TaskStatusSummaryView.as_view(), name='task-status-summary'),
    path('tasks/assigned-tasks/', AssignedTasksView.as_view(), name='assigned-tasks'),
        path('tasks/completion-monthly-aggregation/', TaskCompletionMonthlyAggregationView.as_view(), name='task-completion-monthly-aggregation'),
    path('tasks/<int:pk>/complete_task/', TaskCompletionView.as_view(), name='task-complete'),

    path('dashboard/task-completion/', views.predict_task_completion, name='predict_task_completion'),

path('attendance/employee_today/', views.employee_today, name='employee_today_attendance'),

    # Existing URLs for the manager dashboard
    path('employee/attendance/today/', views.today, name='today_attendance'),
    path('employee/attendance/particular_date/', views.particular_date, name='particular_date_attendance'),
    path('employee/attendance/export_pdf/', views.export_pdf, name='export_attendance_pdf'),
    path('employee/attendance/present_count/', views.present_count, name='present_count'),
    path('employee/attendance/late_arrivals_count/', views.late_arrivals_count, name='late_arrivals_count'),
    path('employee/attendance/absent_count/', views.absent_count, name='absent_count'),

 path('employee/attendance/today/', CompanyTodayAttendanceView.as_view(), name='company-today-attendance'),
    path('employee/attendance/particular_date/', AttendanceByDateView.as_view(), name='company-daily-attendance'),
    
    # Employee-level APIs
    path('employee/attendance/employee_today/', EmployeeTodayAttendanceView.as_view(), name='employee-today-attendance'),
    path('employee/attendance/employee_particular_date/', EmployeeAttendanceByDateView.as_view(), name='employee-daily-attendance'),


    # This URL pattern correctly handles the frontend's request to /api/employee/task/employee-tasks/
    # path('employee/task/employee-tasks/', EmployeeTasksView.as_view(), name='employee-tasks'),
    # path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    # path('taskss/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

path('employee/attendance/weekly-employee-summary/', views.weekly_employee_summary_by_name, name='weekly_employee_summary_by_name'),


    path('managers/personallist/employees/', EmployeeListView.as_view(), name='employee-list'),
    path('personallist/', PersonnelListView.as_view(), name='personnel-list'),

     path('settings/company/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('employee-tasks/', views.get_employee_tasks, name='get_employee_tasks'),

path("employee-tasks/", views.get_employee_tasks, name="employee-tasks"),
    path("employee/tasks/<int:task_id>/", views.update_task_status, name="update-task-status"),
    path('employee/task/employee-tasks/', EmployeeTaskListView.as_view(), name='employee-task-list'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('settings/company/<int:pk>/', CompanyDetail.as_view(), name='company-detail'),
        path('settings/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('predict/task-capacity/', TaskCapacityPredictionView.as_view(), name='task-capacity-prediction'),
    path('get_tasks/', get_user_tasks, name='get-user-tasks'),
    path('task-bonus-prediction/', TaskBonusPredictionAPIView.as_view(), name='task_bonus_prediction'),
path('overall-bonus-prediction/',OverallBonusPredictionAPIView.as_view(),name="overall_bonus_prediction")
,

path('attendance/monthly-metrics/', views.monthly_metrics, name='monthly_metrics'),
    path('attendance/monthly-attendance-summary/', views.monthly_attendance_summary, name='monthly_attendance_summary'),
    path('attendance/monthly-daily-ratio/', views.monthly_daily_ratio, name='monthly_daily_ratio'),
    path('attendance/monthly-punctuality-ratio/', views.monthly_punctuality_ratio, name='monthly_punctuality_ratio'),
    path('attendance/export-monthly-report/', views.export_monthly_report, name='export_monthly_report'),

]