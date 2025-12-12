with open("blog/templates/blog/base.html", "r") as f:
    content = f.read()
content = content.replace("<main>\n        <p>This is the base template for the blog.</p>\n    </main>", "{% block content %}{% endblock %}")
with open("blog/templates/blog/base.html", "w") as f:
    f.write(content)
