def navigation_context(request):
    context = {
        'unread_notifications_count': 0,
    }
    if request.user.is_authenticated and hasattr(request.user, 'notifications'):
        try:
            context['unread_notifications_count'] = request.user.notifications.filter(is_read=False).count()
        except Exception:
            pass
    return context
