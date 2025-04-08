import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Setup Jinja environment
env = Environment(loader=FileSystemLoader("templates"))

# Create output directory
output_dir = Path("_site")
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir()

# Ensure static directory exists in output
static_output = output_dir / "static"
static_output.mkdir()

# Copy static files
if os.path.exists("static"):
    for item in os.listdir("static"):
        s = os.path.join("static", item)
        d = os.path.join(static_output, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

# Generate home page
template = env.get_template("home.html")
with open(output_dir / "index.html", "w") as f:
    f.write(template.render(request={"url_for": lambda name, path: f"/static/{path}"}))

# Generate about page
template = env.get_template("about.html")
about_dir = output_dir / "about"
about_dir.mkdir()
with open(about_dir / "index.html", "w") as f:
    f.write(template.render(request={"url_for": lambda name, path: f"/static/{path}"}))

# Generate projects page
template = env.get_template("projects.html")
projects_dir = output_dir / "projects"
projects_dir.mkdir()
with open(projects_dir / "index.html", "w") as f:
    f.write(template.render(request={"url_for": lambda name, path: f"/static/{path}"}))

# Generate blog page
template = env.get_template("blog.html")
blog_dir = output_dir / "blog"
blog_dir.mkdir()
with open(blog_dir / "index.html", "w") as f:
    f.write(template.render(request={"url_for": lambda name, path: f"/static/{path}"}))

print("Static site generated in _site directory")
