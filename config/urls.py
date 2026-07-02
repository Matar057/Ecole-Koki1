from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls', namespace='dashboard')),
    path('accounts/', include('users.urls', namespace='users')),
    path('students/', include('students.urls', namespace='students')),
    path('teachers/', include('teachers.urls', namespace='teachers')),
    path('academics/', include('academics.urls', namespace='academics')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('fees/', include('fees.urls', namespace='fees')),
    path('timetable/', include('timetable.urls', namespace='timetable')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
