from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from .models import *
from .forms import ContactForm
def shared(): return {"profile":Profile.objects.first(),"site":WebsiteSettings.objects.first(),"social_links":SocialLink.objects.filter(is_public=True)}
def home(request):
 ctx=shared(); ctx.update({"form":ContactForm(),"skills":Skill.objects.filter(is_public=True).select_related("category"),"skill_categories":SkillCategory.objects.all(),"projects":Project.objects.filter(published=True).prefetch_related("technologies")[:6],"certificates":Certificate.objects.filter(is_public=True),"education":Education.objects.filter(is_public=True),"experience":Experience.objects.filter(is_public=True),"achievements":Achievement.objects.filter(is_public=True)})
 return render(request,"portfolio/home.html",ctx)
def projects(request):
 qs=Project.objects.filter(published=True).prefetch_related("technologies"); category=request.GET.get("category",""); query=request.GET.get("q","")
 if category: qs=qs.filter(category=category)
 if query: qs=qs.filter(Q(title__icontains=query)|Q(short_description__icontains=query)|Q(technologies__name__icontains=query)).distinct()
 page=Paginator(qs,9).get_page(request.GET.get("page")); ctx=shared(); ctx.update({"page":page,"categories":Project.CATEGORY,"selected_category":category,"query":query}); return render(request,"portfolio/projects.html",ctx)
def project_detail(request,slug):
 project=get_object_or_404(Project.objects.prefetch_related("technologies","screenshots"),slug=slug,published=True); ctx=shared(); ctx["project"]=project; return render(request,"portfolio/project_detail.html",ctx)
@ratelimit(key="ip",rate="5/h",method="POST",block=True)
@require_http_methods(["GET","POST"])
def contact(request):
 form=ContactForm(request.POST or None)
 if request.method=="POST" and form.is_valid():
  obj=form.save()
  if settings.CONTACT_NOTIFY_EMAIL: send_mail(f"Portfolio contact: {obj.subject}",f"From {obj.name} <{obj.email}>\n\n{obj.message}",settings.DEFAULT_FROM_EMAIL,[settings.CONTACT_NOTIFY_EMAIL],fail_silently=True)
  messages.success(request,"Thanks for reaching out. Your message has been received."); return redirect("home")
 ctx=shared(); ctx["form"]=form; return render(request,"portfolio/contact.html",ctx)
def robots(request): return HttpResponse("User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: /sitemap.xml\n",content_type="text/plain")
def sitemap(request):
 from django.urls import reverse
 from django.utils.html import escape
 base=request.build_absolute_uri("/").rstrip("/"); urls=[base+reverse("home"),base+reverse("projects")]+[base+reverse("project_detail",args=[p.slug]) for p in Project.objects.filter(published=True)]
 return HttpResponse('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f"<url><loc>{escape(u)}</loc></url>" for u in urls)+'</urlset>',content_type="application/xml")
