# PlantGuard AI — Vercel Deployment

This is the Vercel-ready version of the Plant Disease Detection website.

## 1. Put your model files here

Place these two files in the project root:

- `plant_disease_model.keras`
- `class_names.json`

The `class_names.json` file should contain the same 15 class names used during training.

If the files are still in Google Colab:

```python
from google.colab import files
files.download('/content/plant_disease_model.keras')
files.download('/content/class_names.json')
```

## 2. Test locally (optional)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Then:

```bash
flask --app api.index run
```

Open `http://127.0.0.1:5000`.

## 3. Deploy with Vercel

### GitHub method
1. Create a new GitHub repository.
2. Upload the entire contents of this folder.
3. Go to Vercel and choose **New Project**.
4. Import the GitHub repository.
5. Framework preset: **Other**.
6. Leave Build Command and Output Directory empty.
7. Deploy.

### Vercel CLI method

```bash
npm install -g vercel
vercel login
vercel
vercel --prod
```

## Important: large Python function

TensorFlow makes the deployment package large. If Vercel reports a function/package-size limit, enable Vercel's large-functions beta for the project as described in Vercel's current documentation, then redeploy.

## Architecture

- `api/index.py` — Flask prediction API
- `public/index.html` — website
- `public/style.css` — UI styling
- `public/script.js` — upload/prediction frontend
- `plant_disease_model.keras` — trained MobileNetV2 model
- `class_names.json` — 15 output classes
- `vercel.json` — Vercel function configuration

Training remains in Google Colab. Vercel only performs inference on uploaded images.
