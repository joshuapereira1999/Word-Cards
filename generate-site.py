import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader

# Load Excel
df = pd.read_excel("words.xlsx")

# Create output folder
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Load Jinja2 template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("template.html")

# Group by Semantic Domain
for domain, group in df.groupby("semantic domain"):
    words = []
    for _, row in group.iterrows():
        words.append({
            "miriwoong": row["miriwoong"],
            "english": row["english"],
            "class": row["class"],
            "image": row.get("image", ""),
            "audio": row.get("audio", ""),
            "example": row.get("example", ""),
            "translation": row.get("translation", "")
        })
    
    # Render HTML
    html_content = template.render(title=domain, heading=domain, words=words)

    # Write to file (slugify domain for filename)
    filename = f"{domain.replace(' ', '_').lower()}.html"
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Created {filename}")
