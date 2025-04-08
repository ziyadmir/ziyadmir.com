import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Setup Jinja environment with better template handling
env = Environment(loader=FileSystemLoader("templates"))

# Create output directory
output_dir = Path("_site")
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir()

# Copy CNAME file if it exists
if os.path.exists("CNAME"):
    shutil.copy2("CNAME", output_dir / "CNAME")
    print("Copied CNAME file to output directory")

# Copy .nojekyll file to prevent Jekyll processing
with open(output_dir / ".nojekyll", "w") as f:
    f.write("")
print("Created .nojekyll file")

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
    print(f"Copied static files from 'static' directory")
else:
    # Create a simple CSS file to ensure static directory isn't empty
    with open(static_output / "base.css", "w") as f:
        f.write("/* Base styles */\n")
    print("Created placeholder static file")

# Mock request object to simulate FastAPI context
class MockRequest:
    def __init__(self):
        pass
    
    def url_for(self, name, path):
        return f"/static/{path}"

mock_request = {"request": MockRequest()}

# Generate home page
template = env.get_template("home.html")
with open(output_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(template.render(request=mock_request))
print("Generated index.html (home page)")

# Generate about page
template = env.get_template("about.html")
about_dir = output_dir / "about"
about_dir.mkdir()
with open(about_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(template.render(request=mock_request))
print("Generated about/index.html")

# Generate projects page
template = env.get_template("projects.html")
projects_dir = output_dir / "projects"
projects_dir.mkdir()
with open(projects_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(template.render(request=mock_request))
print("Generated projects/index.html")

# Generate blog page
template = env.get_template("blog.html")
blog_dir = output_dir / "blog"
blog_dir.mkdir()
with open(blog_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(template.render(request=mock_request))
print("Generated blog/index.html")

print("\nStatic site successfully generated in _site directory")
