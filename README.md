# Land Use Land Cover Classification using U-Net

This project uses satellite images from 1994 to 2023 to classify land into different categories like water, urban areas, vegetation, etc., using a deep learning model called **U-Net**.

It also includes a **dashboard** that shows how land use has changed over time.

---

## 🔧 What This Project Does

- **Satellite Image Segmentation**: Uses a U-Net model (TensorFlow/Keras) to classify land types.
- **Change Analysis**: Analyzes pixel-wise distribution to track land-use changes over decades.
- **Interactive Dashboard**: Visualizes results with Plotly/Dash charts and trend lines.

---

## 📁 Project Structure

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

## ▶️ How to Run

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

## 📊 Outputs
- **`unet_best_model.h5`**: The weights of the trained segmentation model.
- **`area_analysis1.csv`**: Data file containing area percentages per land class per year.
- **Interactive Graphs**: Pie charts and trend lines showing environmental changes over time.

---

## 📬 Contact
Made by **Sarvan D Suvarna**  
GitHub: [Sarvan-12](https://github.com/Sarvan-12)

---

## 📄 License
This project is under the **MIT License**.
