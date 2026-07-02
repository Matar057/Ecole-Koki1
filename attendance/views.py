from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
import datetime
import xlsxwriter
from .models import Attendance
from .forms import AttendanceForm, BulkAttendanceForm
from users.decorators import role_required
from students.models import Student
from academics.models import Class


@login_required
def attendance_list(request):
    date = request.GET.get('date', datetime.date.today().isoformat())
    class_id = request.GET.get('class')
    attendances = Attendance.objects.filter(date=date).select_related('student')
    if class_id:
        attendances = attendances.filter(student__class_enrolled_id=class_id)
    classes = Class.objects.all()
    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances,
        'date': date,
        'classes': classes,
        'selected_class': class_id,
    })


@role_required('admin', 'teacher')
def attendance_take(request):
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            class_id = request.POST.get('class_id')
            class_obj = get_object_or_404(Class, pk=class_id)
            students = Student.objects.filter(class_enrolled=class_obj, is_active=True)
            for student in students:
                status = request.POST.get(f'attendance_{student.pk}', 'present')
                Attendance.objects.update_or_create(
                    student=student, date=date,
                    defaults={'status': status, 'recorded_by': request.user}
                )
            messages.success(request, 'Présence enregistrée avec succès.')
            return redirect('attendance:attendance_list')
    else:
        form = BulkAttendanceForm(initial={'date': datetime.date.today()})
    classes = Class.objects.all()
    return render(request, 'attendance/attendance_take.html', {'form': form, 'classes': classes})


@login_required
def attendance_report(request):
    start_date = request.GET.get('start_date', datetime.date.today().replace(day=1).isoformat())
    end_date = request.GET.get('end_date', datetime.date.today().isoformat())
    class_id = request.GET.get('class')
    attendances = Attendance.objects.filter(date__range=[start_date, end_date]).select_related('student')
    if class_id:
        attendances = attendances.filter(student__class_enrolled_id=class_id)
    classes = Class.objects.all()
    summary = attendances.values('status').annotate(count=Count('id'))
    return render(request, 'attendance/attendance_report.html', {
        'attendances': attendances,
        'summary': summary,
        'start_date': start_date,
        'end_date': end_date,
        'classes': classes,
    })


@role_required('admin', 'teacher')
def attendance_export(request):
    date = request.GET.get('date', datetime.date.today().isoformat())
    attendances = Attendance.objects.filter(date=date).select_related('student__user')
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=attendance_{date}.xlsx'
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.write_row(0, 0, ['ID Étudiant', 'Nom', 'Classe', 'Statut', 'Date'], bold)
    for i, att in enumerate(attendances, 1):
        worksheet.write_row(i, 0, [
            att.student.student_id,
            att.student.user.get_full_name(),
            str(att.student.class_enrolled),
            att.get_status_display(),
            str(att.date),
        ])
    workbook.close()
    return response
