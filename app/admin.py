from django.contrib import admin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import AuthorRequest, Post, Category

class AuthorRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_approved', 'request_date']
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for req in queryset:
            req.user.is_author = True
            req.user.save()
            req.is_approved = True
            req.save()
            subject = 'Author Request Approved'
            from_email = 'contact@helphash.org'
            to_email = [req.user.email]
            html_content = render_to_string('email/author_request_approved.html', {'user': req.user})
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    def reject_requests(self, request, queryset):
        for req in queryset:
            subject = 'Author Request Rejected'
            from_email = 'contact@helphash.org'
            to_email = [req.user.email]
            html_content = render_to_string('email/author_request_rejected.html', {'user': req.user})
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            req.delete()

admin.site.register(AuthorRequest, AuthorRequestAdmin)
admin.site.register(Post)
admin.site.register(Category)