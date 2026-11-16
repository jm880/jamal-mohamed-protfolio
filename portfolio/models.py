from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.utils.text import slugify

class Profile(models.Model):
    full_name=models.CharField(max_length=120,default="Jamal Mohamed")
    headline=models.CharField(max_length=180,blank=True)
    hero_subtitle=models.CharField(max_length=240,blank=True)
    biography=models.TextField(blank=True)
    academic_background=models.TextField(blank=True)
    specialization=models.CharField(max_length=180,blank=True)
    interests=models.TextField(blank=True)
    career_objectives=models.TextField(blank=True)
    learning_journey=models.TextField(blank=True)
    location=models.CharField(max_length=120,blank=True)
    photo=models.ImageField(upload_to="profile/",blank=True,validators=[FileExtensionValidator(["jpg","jpeg","png","webp"])])
    resume=models.FileField(upload_to="resume/",blank=True,validators=[FileExtensionValidator(["pdf"])])
    available=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: verbose_name="Profile"
    def __str__(self): return self.full_name
    def save(self,*args,**kwargs):
        if not self.pk and Profile.objects.exists(): self.pk=Profile.objects.first().pk
        super().save(*args,**kwargs)

class SocialLink(models.Model):
    label=models.CharField(max_length=60); url=models.URLField(blank=True); phone_number=models.CharField(max_length=30,blank=True); sort_order=models.PositiveIntegerField(default=0); is_public=models.BooleanField(default=True)
    class Meta: ordering=["sort_order","label"]
    def __str__(self): return self.label
    @property
    def target_url(self):
        if self.phone_number and self.label.lower()=="whatsapp": return "https://wa.me/"+"".join(c for c in self.phone_number if c.isdigit())
        return self.url

class SkillCategory(models.Model):
    name=models.CharField(max_length=80,unique=True); sort_order=models.PositiveIntegerField(default=0)
    class Meta: ordering=["sort_order","name"]; verbose_name_plural="Skill categories"
    def __str__(self): return self.name
class Skill(models.Model):
    name=models.CharField(max_length=100); category=models.ForeignKey(SkillCategory,on_delete=models.CASCADE,related_name="skills"); proficiency=models.PositiveSmallIntegerField(null=True,blank=True,validators=[MinValueValidator(0),MaxValueValidator(100)]); sort_order=models.PositiveIntegerField(default=0); is_public=models.BooleanField(default=True)
    class Meta: ordering=["sort_order","name"]; unique_together=[("name","category")]
    def __str__(self): return self.name
class Technology(models.Model):
    name=models.CharField(max_length=80,unique=True)
    def __str__(self): return self.name
class Project(models.Model):
    CATEGORY=[(x,x) for x in ["Cybersecurity","Artificial Intelligence","Web Development","Python","Programming","Other"]]
    title=models.CharField(max_length=160); slug=models.SlugField(unique=True,blank=True); short_description=models.CharField(max_length=260,blank=True); description=models.TextField(blank=True); image=models.ImageField(upload_to="projects/",blank=True,validators=[FileExtensionValidator(["jpg","jpeg","png","webp"])])
    category=models.CharField(max_length=40,choices=CATEGORY,default="Other"); technologies=models.ManyToManyField(Technology,blank=True); github_url=models.URLField(blank=True); demo_url=models.URLField(blank=True); completion_date=models.DateField(null=True,blank=True); featured=models.BooleanField(default=False); published=models.BooleanField(default=False); sort_order=models.PositiveIntegerField(default=0); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["sort_order","-featured","-completion_date"]
    def __str__(self): return self.title
    def save(self,*args,**kwargs):
        if not self.slug: self.slug=slugify(self.title)[:50]
        super().save(*args,**kwargs)
class ProjectImage(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="screenshots"); image=models.ImageField(upload_to="projects/screenshots/",validators=[FileExtensionValidator(["jpg","jpeg","png","webp"])]); caption=models.CharField(max_length=180,blank=True); sort_order=models.PositiveIntegerField(default=0)
    class Meta: ordering=["sort_order"]
class Certificate(models.Model):
    title=models.CharField(max_length=180); organization=models.CharField(max_length=160,blank=True); issue_date=models.DateField(null=True,blank=True); credential_id=models.CharField(max_length=120,blank=True); verification_url=models.URLField(blank=True); file=models.FileField(upload_to="certificates/",blank=True,validators=[FileExtensionValidator(["jpg","jpeg","png","webp","pdf"])]); description=models.TextField(blank=True); category=models.CharField(max_length=100,blank=True); is_public=models.BooleanField(default=False); sort_order=models.PositiveIntegerField(default=0)
    class Meta: ordering=["sort_order","-issue_date"]
    def __str__(self): return self.title
class Education(models.Model):
    institution=models.CharField(max_length=180); program=models.CharField(max_length=180,blank=True); field_of_study=models.CharField(max_length=160,blank=True); start_date=models.DateField(null=True,blank=True); end_date=models.DateField(null=True,blank=True); description=models.TextField(blank=True); sort_order=models.PositiveIntegerField(default=0); is_public=models.BooleanField(default=True)
    class Meta: ordering=["sort_order","-start_date"]
    def __str__(self): return self.institution
class Experience(models.Model):
    organization=models.CharField(max_length=180); position=models.CharField(max_length=160,blank=True); start_date=models.DateField(null=True,blank=True); end_date=models.DateField(null=True,blank=True); responsibilities=models.TextField(blank=True); skills_gained=models.CharField(max_length=240,blank=True); sort_order=models.PositiveIntegerField(default=0); is_public=models.BooleanField(default=True)
    class Meta: ordering=["sort_order","-start_date"]
    def __str__(self): return self.organization
class Achievement(models.Model):
    title=models.CharField(max_length=180); description=models.TextField(blank=True); date=models.DateField(null=True,blank=True); category=models.CharField(max_length=80,blank=True); sort_order=models.PositiveIntegerField(default=0); is_public=models.BooleanField(default=True)
    class Meta: ordering=["sort_order","-date"]
    def __str__(self): return self.title
class ContactMessage(models.Model):
    name=models.CharField(max_length=100); email=models.EmailField(); subject=models.CharField(max_length=160); message=models.TextField(max_length=5000); created_at=models.DateTimeField(auto_now_add=True); is_read=models.BooleanField(default=False)
    class Meta: ordering=["-created_at"]
    def __str__(self): return f"{self.subject} — {self.name}"
class WebsiteSettings(models.Model):
    site_title=models.CharField(max_length=160,default="Jamal Mohamed | Cybersecurity"); meta_description=models.CharField(max_length=300,blank=True); footer_text=models.CharField(max_length=200,blank=True); background_image=models.ImageField(upload_to="site/",blank=True,validators=[FileExtensionValidator(["jpg","jpeg","png","webp"]) ]); background_video=models.FileField(upload_to="site/",blank=True,validators=[FileExtensionValidator(["mp4","webm"]) ]); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.site_title
    def save(self,*args,**kwargs):
        if not self.pk and WebsiteSettings.objects.exists(): self.pk=WebsiteSettings.objects.first().pk
        super().save(*args,**kwargs)
