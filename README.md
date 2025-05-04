# Land Use Land Cover Classification using U-Net

This project uses satellite images from 1994 to 2023 to classify land into different categories like water, urban areas, vegetation, etc., using a deep learning model called **U-Net**.

It also includes a **dashboard** that shows how land use has changed over time.

---

## 🔧 What This Project Does

- Uses satellite images (TIFF files)
- Segments the land into classes using a U-Net model
- Analyzes how land use changes over time
- Shows the results in a dashboard with graphs and pie charts

---

## 📁 Folders and Files

```
├── data/                # Contains raw and processed data
├── models/              # Trained model files (.h5 and .pkl)
├── scripts/             # Python files for preprocessing, training, prediction
├── dash_app/            # Dash dashboard app
├── notebooks/           # Optional Jupyter notebooks for testing
├── requirements.txt     # All required Python packages
└── README.md            # This file
```

---

## ▶️ How to Run

### 1. Install everything
```bash
pip install -r requirements.txt
```

### 2. Preprocess data
```bash
python scripts/preprocess.py
```

### 3. Train the model
```bash
python scripts/train_unet.py
```

### 4. Predict and analyze
```bash
python scripts/predict.py
python scripts/analyze.py
```

### 5. Run the dashboard
```bash
cd dash_app
python dash1.py
```
Then go to `http://127.0.0.1:8050` in your browser.

---

## 📊 Output

- `area_by_class.csv`: Land use area per class per year
- `dash1.py`: Dashboard with charts showing land use change over time

---

## 📬 Contact

Made by **Sarvan D Suvarna**  
GitHub: [Sarvan-12](https://github.com/Sarvan-12)

---

## 📄 License

This project is under the **MIT License** – free to use, modify, and share.
