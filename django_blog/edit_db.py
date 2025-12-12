with open("django_blog/settings.py", "r") as f:
    content = f.read()
content = content.replace("'ENGINE': 'django.db.backends.sqlite3',\n        'NAME': BASE_DIR / 'db.sqlite3',\n    ", "'ENGINE': 'django.db.backends.postgresql',\n        'NAME': 'django_blog',\n        'USER': 'postgres',\n        'PASSWORD': 'password',\n        'HOST': 'localhost',\n        'PORT': '5432',\n    ")
with open("django_blog/settings.py", "w") as f:
    f.write(content)
