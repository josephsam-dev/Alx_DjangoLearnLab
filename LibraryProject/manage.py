# 1) Ensure we're in the project root (manage.py should be here)
pwd
ls -la manage.py || { echo "Stop: run this from the folder that contains manage.py"; exit 1; }

# 2) Ensure package file exists
touch relationship_app/__init__.py

# 3) Write a canonical apps.py
cat > relationship_app/apps.py <<'PY'
from django.apps import AppConfig

class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'
PY

# 4) Write the models.py (ForeignKey, ManyToMany, OneToOne)
cat > relationship_app/models.py <<'PY'
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='libraries', blank=True)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return f"{self.name} — {self.library.name}"
PY

# 5) Quick show to confirm files
echo "---- relationship_app listing ----"
ls -la relationship_app
echo "---- head of apps.py ----"
sed -n '1,120p' relationship_app/apps.py
echo "---- head of models.py ----"
sed -n '1,240p' relationship_app/models.py

# 6) Ensure settings.py contains relationship_app (show the INSTALLED_APPS block)
echo "---- INSTALLED_APPS in settings.py ----"
sed -n '/INSTALLED_APPS = \\[/,/]/{p}' LibraryProject/settings.py

# 7) Make migrations specifically for relationship_app and apply
python manage.py makemigrations relationship_app
python manage.py migrate
