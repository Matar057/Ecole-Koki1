from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import JsonResponse
from .models import Student, Parent, StudentDocument
from .forms import StudentForm, StudentDocumentForm
from users.decorators import role_required

User = get_user_model()


def student_list_ajax(request):
    class_id = request.GET.get('class')
    students = Student.objects.filter(is_active=True)
    if class_id:
        students = students.filter(class_enrolled_id=class_id)
    data = [{'id': s.pk, 'name': s.user.get_full_name()} for s in students]
    return JsonResponse(data, safe=False)


@login_required
def student_list(request):
    students = Student.objects.select_related('user', 'class_enrolled', 'section', 'parent').all()
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    documents = student.documents.all()
    attendance_rate = None
    total_attendance = student.attendance_records.count()
    if total_attendance > 0:
        present = student.attendance_records.filter(status='present').count()
        attendance_rate = round((present / total_attendance) * 100, 1)
    return render(request, 'students/student_detail.html', {
        'student': student,
        'documents': documents,
        'attendance_rate': attendance_rate,
    })


@role_required('admin', 'teacher')
def student_create(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES)
        if student_form.is_valid():
            student = student_form.save(commit=False)
            email = request.POST.get('student_email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            if email and first_name and last_name:
                user = User.objects.create_user(
                    username=email.split('@')[0],
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role='student',
                    password='student123'
                )
                student.user = user

                parent_full_name = request.POST.get('parent_full_name', '').strip()
                parent_phone = request.POST.get('parent_phone', '').strip()
                if parent_full_name:
                    parts = parent_full_name.split(' ', 1)
                    p_first = parts[0]
                    p_last = parts[1] if len(parts) > 1 else ''
                    parent_email = f"parent_{p_last}_{p_first}@koki1.local".lower()
                    parent_user, created = User.objects.get_or_create(
                        email=parent_email,
                        defaults={
                            'username': f"parent_{p_last}_{p_first}".lower(),
                            'first_name': p_first,
                            'last_name': p_last,
                            'role': 'parent',
                            'password': 'parent123',
                        }
                    )
                    if created:
                        parent_user.set_password('parent123')
                        parent_user.save()
                    parent_obj, _ = Parent.objects.get_or_create(
                        user=parent_user,
                        defaults={'phone': parent_phone}
                    )
                    if parent_phone and not parent_obj.phone:
                        parent_obj.phone = parent_phone
                        parent_obj.save()
                    student.parent = parent_obj

                student.save()
                messages.success(request, 'Étudiant créé avec succès.')
                return redirect('students:student_list')
    else:
        student_form = StudentForm()
    return render(request, 'students/student_form.html', {
        'student_form': student_form,
        'title': 'Ajouter un étudiant',
    })


@role_required('admin', 'teacher')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()

            parent_full_name = request.POST.get('parent_full_name', '').strip()
            parent_phone = request.POST.get('parent_phone', '').strip()
            if parent_full_name:
                parts = parent_full_name.split(' ', 1)
                p_first = parts[0]
                p_last = parts[1] if len(parts) > 1 else ''
                parent_email = f"parent_{p_last}_{p_first}@koki1.local".lower()
                parent_user, created = User.objects.get_or_create(
                    email=parent_email,
                    defaults={
                        'username': f"parent_{p_last}_{p_first}".lower(),
                        'first_name': p_first,
                        'last_name': p_last,
                        'role': 'parent',
                        'password': 'parent123',
                    }
                )
                if created:
                    parent_user.set_password('parent123')
                    parent_user.save()
                parent_obj, _ = Parent.objects.get_or_create(
                    user=parent_user,
                    defaults={'phone': parent_phone}
                )
                if parent_phone and not parent_obj.phone:
                    parent_obj.phone = parent_phone
                    parent_obj.save()
                student.parent = parent_obj
                student.save()
            elif not student.parent and not parent_full_name:
                pass

            messages.success(request, 'Étudiant mis à jour avec succès.')
            return redirect('students:student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
        if student.parent:
            form.fields['parent_full_name'].initial = student.parent.user.get_full_name()
            form.fields['parent_phone'].initial = student.parent.phone
    return render(request, 'students/student_form.html', {
        'student_form': form,
        'title': 'Modifier l\'étudiant',
    })


@role_required('admin')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, 'Étudiant supprimé avec succès.')
        return redirect('students:student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@role_required('admin', 'teacher')
def document_upload(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.student = student
            doc.save()
            messages.success(request, 'Document téléversé avec succès.')
            return redirect('students:student_detail', pk=pk)
    else:
        form = StudentDocumentForm()
    return render(request, 'students/document_upload.html', {'form': form, 'student': student})
