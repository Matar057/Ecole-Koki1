from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Teacher
from .forms import TeacherForm
from users.decorators import role_required

User = get_user_model()


@login_required
def teacher_list(request):
    teachers = Teacher.objects.select_related('user').prefetch_related('subjects', 'classes_assigned').all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})


@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})


@role_required('admin')
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            user = User.objects.create_user(
                username=form.cleaned_data.get('email', '').split('@')[0] if form.cleaned_data.get('email') else teacher.teacher_id,
                email=form.cleaned_data.get('email', ''),
                first_name=request.POST.get('first_name', 'Teacher'),
                last_name=request.POST.get('last_name', ''),
                role='teacher',
            )
            teacher.user = user
            teacher.save()
            form.save_m2m()
            messages.success(request, 'Enseignant créé avec succès.')
            return redirect('teachers:teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Ajouter un enseignant'})


@role_required('admin')
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enseignant mis à jour avec succès.')
            return redirect('teachers:teacher_detail', pk=pk)
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Modifier l\'enseignant'})


@role_required('admin')
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        user = teacher.user
        teacher.delete()
        user.delete()
        messages.success(request, 'Enseignant supprimé avec succès.')
        return redirect('teachers:teacher_list')
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})
