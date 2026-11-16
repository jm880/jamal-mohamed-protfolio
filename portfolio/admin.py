from django.contrib import admin
from .models import *
admin.site.site_header="Jamal Mohamed · Portfolio CMS"
admin.site.site_title="Portfolio administration"
admin.site.index_title="Manage portfolio content"
class ScreenshotInline(admin.TabularInline): model=ProjectImage; extra=1
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin): list_display=("title","category","published","featured","completion_date"); list_filter=("published","featured","category"); search_fields=("title","description"); prepopulated_fields={"slug":("title",)}; filter_horizontal=("technologies",); inlines=[ScreenshotInline]
@admin.register(ContactMessage)
class MessageAdmin(admin.ModelAdmin): list_display=("subject","name","email","created_at","is_read"); list_filter=("is_read","created_at"); search_fields=("name","email","subject","message"); readonly_fields=("name","email","subject","message","created_at")
for model in [Profile,SocialLink,SkillCategory,Skill,Technology,ProjectImage,Certificate,Education,Experience,Achievement,WebsiteSettings]:
    try: admin.site.register(model)
    except admin.sites.AlreadyRegistered: pass
