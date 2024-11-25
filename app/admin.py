from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import AuthorRequest, Post, Category
from .forms import PostAdminForm

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
            req.user.is_author = False
            req.user.save()
            subject = 'Author Request Rejected'
            from_email = 'contact@helphash.org'
            to_email = [req.user.email]
            html_content = render_to_string('email/author_request_rejected.html', {'user': req.user})
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            req.delete()

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    class Media:
        js = ('https://cdn.tiny.cloud/1/nb9wx71qqrxl92bz997hu86loe17fsiz8w5s62x0b4jew7fz/tinymce/5/tinymce.min.js', 'js/tinymce_init.js')

admin.site.register(AuthorRequest, AuthorRequestAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)