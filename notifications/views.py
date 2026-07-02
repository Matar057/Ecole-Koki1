from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Announcement, Notification
from .forms import AnnouncementForm
from users.decorators import role_required

User = get_user_model()


@login_required
def announcement_list(request):
    announcements = Announcement.objects.select_related('created_by').all()
    if not request.user.is_admin:
        announcements = announcements.filter(
            target_audience__in=['all', request.user.role]
        )
    return render(request, 'notifications/announcement_list.html', {'announcements': announcements})


@role_required('admin', 'teacher')
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, 'Annonce créée.')
            audience_map = {
                'students': 'student',
                'teachers': 'teacher',
                'parents': 'parent',
                'admins': 'admin',
                'all': None,
            }
            role_key = audience_map.get(form.cleaned_data['target_audience'])
            target_users = User.objects.filter(role=role_key) if role_key else User.objects.all()
            for user in target_users:
                Notification.objects.create(
                    user=user,
                    title=announcement.title,
                    message=announcement.content,
                    notification_type='announcement',
                )
            return redirect('notifications:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'notifications/announcement_form.html', {'form': form, 'title': 'Nouvelle annonce'})


@login_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'notifications/announcement_detail.html', {'announcement': announcement})


@role_required('admin', 'teacher')
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Annonce mise à jour.')
            return redirect('notifications:announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'notifications/announcement_form.html', {'form': form, 'title': "Modifier l'annonce"})


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})


@login_required
def mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notification_list')


@login_required
def mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    messages.success(request, 'Toutes les notifications marquées comme lues.')
    return redirect('notifications:notification_list')


@role_required('admin', 'teacher')
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Annonce supprimée.')
        return redirect('notifications:announcement_list')
    return render(request, 'notifications/announcement_confirm_delete.html', {'announcement': announcement})
