# PlantGuard AI — Final Vercel Flask Version

This version intentionally has **no `vercel.json`**.

Vercel's current Flask deployment supports zero-configuration framework detection.
The root `app.py` is the Flask application and `/` is the website.

## Structure

```text
app.py
plant_disease_model.keras
class_names.json
requirements.txt
templates/
  index.html
static/
  style.css
  script.js
```

## Deploy

1. Replace the files in your GitHub repository with this project's files.
2. Make sure `app.py` is directly in the repository root.
3. Make sure `plant_disease_model.keras` and `class_names.json` are also directly in the root.
4. Commit and push.
5. Vercel will automatically create a new production deployment.

Do NOT put the project inside another nested folder.

## Expected routes

`/` → PlantGuard website

`/predict` → image prediction API

## If `/` still returns 404

Open Vercel → Project → Settings → General and verify the Root Directory points to the folder containing `app.py`.

Then redeploy.
