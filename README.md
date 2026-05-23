# Land Use Land Cover Classification using U-Net

This project uses satellite images from 1994 to 2023 to classify land into different categories like water, urban areas, vegetation, etc., using a deep learning model called **U-Net**.

It also includes a **dashboard** that shows how land use has changed over time.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;display:inline"><path d="M14.7 6.3l3 3M10.2 4.6l2.3 2.3-8.5 8.5c-.8.8-.8 2 0 2.8l2.1 2.1c.8.8 2 .8 2.8 0l8.5-8.5 2.3 2.3c.4.4 1 .4 1.4 0l.7-.7c.4-.4.4-1 0-1.4l-8-8c-.4-.4-1-.4-1.4 0l-.7.7c-.4.4-.4 1 0 1.4Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> What This Project Does

- **Satellite Image Segmentation**: Uses a U-Net model (TensorFlow/Keras) to classify land types.
- **Change Analysis**: Analyzes pixel-wise distribution to track land-use changes over decades.
- **Interactive Dashboard**: Visualizes results with Plotly/Dash charts and trend lines.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;display:inline"><path d="M3 7v13h18V7M3 7l9-5 9 5M7.5 10.6v.01M7.5 14.6v.01M12 12.6v.01M12 16.6v.01M16.5 10.6v.01M16.5 14.6v.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Project Structure

```
├── data/                # Raw satellite imagery and processed CSV results
├── models/              # Trained U-Net model files (.h5)
├── scripts/             # Python scripts for the entire pipeline
│   ├── preprocess.py    # Image normalization and resizing
│   ├── train_unet.py    # Training logic
│   ├── segment_images.py# Model inference/prediction
│   ├── analyze.py       # Area calculation and CSV generation
│   └── dash1.py         # Dashboard application
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;display:inline"><polygon points="5 3 19 12 5 21 5 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg> How to Run

### 1. Environment Setup
We recommend using a virtual environment (tested on Python 3.10 - 3.12).
```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Preprocess Data
Prepare the raw TIFF images for the model.
```bash
python scripts/preprocess.py
```

### 3. Train the Model (Optional)
If you want to re-train the U-Net model:
```bash
python scripts/train_unet.py
```

### 4. Segment and Analyze
Run inference on images and generate the area analysis CSV.
```bash
python scripts/segment_images.py
python scripts/analyze.py
```

### 5. Run the Dashboard
Launch the interactive web visualization.
```bash
python scripts/dash1.py
```
Then open [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

---

## <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;display:inline"><path d="M3 3v18h18V3H3zm3 6h12M9 21V9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 21V9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Outputs

- **`unet_best_model.h5`**: The weights of the trained segmentation model.
- **`area_analysis1.csv`**: Data file containing area percentages per land class per year.
- **Interactive Graphs**: Pie charts and trend lines showing environmental changes over time.

---

<div align="center">
  <h3><img src="https://api.iconify.design/lucide/star.svg?color=%237850ff" width="22" height="22" align="absmiddle" /> If you like this project or find it helpful, please consider giving it a star!</h3>

  <a href="https://www.linkedin.com/in/sarvan12/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge" />
  </a>
</div>

---

