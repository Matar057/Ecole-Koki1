from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TimetableSlot
from .forms import TimetableSlotForm
from users.decorators import role_required
from academics.models import Class
from teachers.models import Teacher


DAYS = [
    ('monday', 'Lundi'), ('tuesday', 'Mardi'), ('wednesday', 'Mercredi'),
    ('thursday', 'Jeudi'), ('friday', 'Vendredi'), ('saturday', 'Samedi'),
]
TIME_SLOTS = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00']


@login_required
def timetable_list(request):
    classes = Class.objects.all()
    class_id = request.GET.get('class')
    slots = TimetableSlot.objects.select_related('class_obj', 'section', 'subject', 'teacher')
    if class_id:
        slots = slots.filter(class_obj_id=class_id)
    timetable = {}
    for slot in slots:
        if slot.day not in timetable:
            timetable[slot.day] = []
        timetable[slot.day].append(slot)
    for day in timetable:
        timetable[day].sort(key=lambda x: x.start_time)
    return render(request, 'timetable/timetable_list.html', {
        'timetable': timetable,
        'classes': classes,
        'selected_class': class_id,
        'days': DAYS,
        'time_slots': TIME_SLOTS,
    })


@role_required('admin')
def slot_create(request):
    if request.method == 'POST':
        form = TimetableSlotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Créneau créé.')
            return redirect('timetable:timetable_list')
    else:
        form = TimetableSlotForm()
    return render(request, 'timetable/slot_form.html', {'form': form, 'title': 'Ajouter un créneau'})


@role_required('admin')
def slot_edit(request, pk):
    slot = get_object_or_404(TimetableSlot, pk=pk)
    if request.method == 'POST':
        form = TimetableSlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Créneau mis à jour.')
            return redirect('timetable:timetable_list')
    else:
        form = TimetableSlotForm(instance=slot)
    return render(request, 'timetable/slot_form.html', {'form': form, 'title': 'Modifier le créneau'})


@role_required('admin')
def slot_delete(request, pk):
    slot = get_object_or_404(TimetableSlot, pk=pk)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, 'Créneau supprimé.')
        return redirect('timetable:timetable_list')
    return render(request, 'timetable/slot_confirm_delete.html', {'slot': slot})


@login_required
def teacher_timetable(request):
    if request.user.is_teacher:
        teacher = request.user.teacher_profile
    else:
        teacher_id = request.GET.get('teacher')
        teacher = get_object_or_404(Teacher, pk=teacher_id) if teacher_id else None
    slots = TimetableSlot.objects.filter(teacher=teacher).select_related('class_obj', 'subject') if teacher else []
    timetable = {}
    for slot in slots:
        if slot.day not in timetable:
            timetable[slot.day] = []
        timetable[slot.day].append(slot)
    for day in timetable:
        timetable[day].sort(key=lambda x: x.start_time)
    return render(request, 'timetable/teacher_timetable.html', {
        'timetable': timetable,
        'teacher': teacher,
        'days': DAYS,
        'time_slots': TIME_SLOTS,
    })
