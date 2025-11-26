from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from companyusers.models import CompanyUser

@login_required
def notification_list(request):
    company_user = CompanyUser.objects.filter(user=request.user).first()
    if company_user:
        notifications = Notification.objects.filter(company_user=company_user, is_read=False).order_by('-created_at')
    else:
        notifications = Notification.objects.none() # No company user, no notifications

    context = {
        'notifications': notifications
    }
    return render(request, 'notifications.html', context)