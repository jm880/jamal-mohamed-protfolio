# Jamal Mohamed — Cybersecurity Portfolio

Django portfolio with responsive cyber-inspired public pages, project publishing, skills, certificates, education and experience, and a private Django Admin content manager. Personal claims and proficiency levels are not pre-populated.

## Local setup

Requires Python 3.10+. Create and activate a virtual environment, install `pip install -r requirements.txt`, then copy `.env.example` to `.env`. Django does not load `.env` automatically; export those values in your shell or use a deployment secret manager. Set a unique `DJANGO_SECRET_KEY`.

Run `python manage.py makemigrations portfolio`, `python manage.py migrate`, and `python manage.py createsuperuser`. Then run `python manage.py runserver`. Visit `/` and `/admin/`. No public admin registration or shipped credentials exist.

In Admin, add a Profile and fill real details. Add skills and categories; proficiency remains blank unless set. Publish projects explicitly. Only certificates marked public appear. Add a Social Link labeled WhatsApp with a phone number in international format to build its wa.me URL. Contact submissions are saved to the admin inbox.

## Production

Set `DJANGO_DEBUG=False`, a long random `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DB`, and `CSRF_TRUSTED_ORIGINS=https://your-domain`. For mail notifications configure SMTP via `EMAIL_BACKEND`, `DEFAULT_FROM_EMAIL`, and `CONTACT_NOTIFY_EMAIL`. Run `python manage.py migrate` and `python manage.py collectstatic --noinput`; serve the WSGI application behind HTTPS. Persist and back up `media/` or configure controlled object storage. Configure database backups. Secure cookie flags, HTTPS redirect, HSTS and clickjacking/content-type protections activate when DEBUG is false.

## Included functionality

- Django Admin authentication, permission checks, CSRF and Django password hashing.
- CRUD for portfolio models; project technologies and screenshots are supported.
- Contact form validation, honeypot, CSRF, database inbox, configurable notification email and POST rate limit.
- Public project search/category filters, pagination and details.
- Responsive layout with optional canvas code rain, scroll reveal, category filters, hover tilt and reduced-motion support.
- Sitemap and robots endpoints.

The initial schema migration is created using Django's migration command because Django was not installed in the build environment. Run `makemigrations portfolio` once before `migrate`. Certificate image/PDF uploads and project/profile images are extension-restricted; configure host-level upload scanning and storage limits for production.
