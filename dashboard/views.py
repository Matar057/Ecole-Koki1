from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from students.models import Student
from teachers.models import Teacher
from academics.models import Class, Subject
from attendance.models import Attendance
from exams.models import Exam, Mark
from fees.models import FeePayment
from notifications.models import Announcement
import datetime


@login_required
def home(request):
    context = {}
    today = datetime.date.today()
    context['student_count'] = Student.objects.filter(is_active=True).count()
    context['teacher_count'] = Teacher.objects.filter(is_active=True).count()
    context['class_count'] = Class.objects.count()
    context['subject_count'] = Subject.objects.count()
    context['recent_attendance'] = Attendance.objects.filter(date=today).count()
    if context['student_count'] > 0 and context['recent_attendance'] > 0:
        present_today = Attendance.objects.filter(date=today, status='present').count()
        context['attendance_rate'] = round((present_today / context['recent_attendance']) * 100, 1)
    else:
        context['attendance_rate'] = 0
    context['upcoming_exams'] = Exam.objects.filter(start_date__gte=today, is_published=True)[:5]
    context['pending_fees'] = FeePayment.objects.filter(status__in=['pending', 'overdue']).count()
    context['recent_announcements'] = Announcement.objects.filter(is_active=True)[:5]
    context['total_collected'] = FeePayment.objects.filter(status__in=['paid', 'partial']).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    context['total_pending'] = FeePayment.objects.filter(status='pending').aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    students_by_class = Student.objects.filter(is_active=True).values('class_enrolled__name').annotate(count=Count('id')).order_by('class_enrolled__name')
    context['students_by_class'] = list(students_by_class)
    attendance_summary = Attendance.objects.filter(date__gte=today - datetime.timedelta(days=30)).values('status').annotate(count=Count('id'))
    context['attendance_summary'] = {item['status']: item['count'] for item in attendance_summary}
    return render(request, 'dashboard/home.html', context)
