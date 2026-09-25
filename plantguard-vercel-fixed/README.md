# PlantGuard AI — Fixed Vercel Flask Deployment

This version uses Vercel's Flask-style project layout so `/` is served directly by Flask.

## Files
- `app.py` — Flask website + `/predict` API
- `templates/index.html` — frontend
- `static/style.css` — styling
- `static/script.js` — image upload and API call
- `plant_disease_model.keras` — supplied trained model
- `class_names.json` — supplied 15-class list
- `requirements.txt`
- `vercel.json`

## Deploy
Push the complete folder to GitHub, then import the repository into Vercel.

Use:
- Framework Preset: Other
- Build Command: empty
- Output Directory: empty

Then Deploy.

The homepage is `/` and prediction endpoint is `/predict`.

## Important
TensorFlow can make a Python serverless deployment large. If Vercel reports a package/function-size limit, enable the large-function option available for the project/account and redeploy.
