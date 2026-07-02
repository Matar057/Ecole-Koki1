from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import AcademicYear, Class, Section, Subject
from .forms import AcademicYearForm, ClassForm, SectionForm, SubjectForm
from users.decorators import role_required


@login_required
def academic_year_list(request):
    years = AcademicYear.objects.all()
    return render(request, 'academics/academic_year_list.html', {'years': years})


@role_required('admin')
def academic_year_create(request):
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Année académique créée.')
            return redirect('academics:academic_year_list')
    else:
        form = AcademicYearForm()
    return render(request, 'academics/academic_year_form.html', {'form': form, 'title': 'Ajouter une année académique'})


@role_required('admin')
def academic_year_edit(request, pk):
    year = get_object_or_404(AcademicYear, pk=pk)
    if request.method == 'POST':
        form = AcademicYearForm(request.POST, instance=year)
        if form.is_valid():
            form.save()
            messages.success(request, 'Année académique mise à jour.')
            return redirect('academics:academic_year_list')
    else:
        form = AcademicYearForm(instance=year)
    return render(request, 'academics/academic_year_form.html', {'form': form, 'title': 'Modifier l\'année académique'})


@login_required
def class_list(request):
    classes = Class.objects.select_related('academic_year').annotate(num_students=models.Count('students'))
    return render(request, 'academics/class_list.html', {'classes': classes})


@role_required('admin')
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe créée.')
            return redirect('academics:class_list')
    else:
        form = ClassForm()
    return render(request, 'academics/class_form.html', {'form': form, 'title': 'Ajouter une classe'})


@role_required('admin')
def class_edit(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe mise à jour.')
            return redirect('academics:class_list')
    else:
        form = ClassForm(instance=class_obj)
    return render(request, 'academics/class_form.html', {'form': form, 'title': 'Modifier la classe'})


@login_required
def subject_list(request):
    subjects = Subject.objects.prefetch_related('classes', 'teachers').all()
    return render(request, 'academics/subject_list.html', {'subjects': subjects})


@role_required('admin')
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière créée.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'academics/subject_form.html', {'form': form, 'title': 'Ajouter une matière'})


@role_required('admin')
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière mise à jour.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'academics/subject_form.html', {'form': form, 'title': 'Modifier la matière'})


@login_required
def section_list(request):
    sections = Section.objects.select_related('class_obj').all()
    return render(request, 'academics/section_list.html', {'sections': sections})


@role_required('admin')
def section_create(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section créée.')
            return redirect('academics:section_list')
    else:
        form = SectionForm()
    return render(request, 'academics/section_form.html', {'form': form, 'title': 'Ajouter une section'})
