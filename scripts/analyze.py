import os
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image

# =================== Utility Functions ===================

def get_classes_from_image(image_path):
    """
    Reads a segmentation mask and returns unique classes and the image array.
    """
    img = Image.open(image_path)
    img_array = np.array(img)
    unique_classes = np.unique(img_array)
    return unique_classes, img_array

def get_area_data(region, year):
    """
    Calculates pixel-wise area of each class for a given region and year.
    """
    region_path = Path(f'data/raw/{region}')
    image_files = list(region_path.glob(f'*_{year}.tif'))

    if not image_files:
        print(f"No image found for {region} in {year}")
        return None

    image_file = image_files[0]
    classes, img_array = get_classes_from_image(image_file)
    areas = {cls: np.sum(img_array == cls) for cls in classes}
    return areas

def get_years(region):
    """
    Extracts all years from filenames in a region folder.
    """
    region_dir = Path(f'data/raw/{region}')
    image_files = list(region_dir.glob('*.tif'))

    years = set()
    for image in image_files:
        try:
            year = int(image.stem.split('_')[-1])
            years.add(year)
        except ValueError:
            continue
    return sorted(years)

def analyze_region(region):
    """
    Analyzes all years for a given region and returns area data.
    """
    years = get_years(region)
    analysis_results = []

    for year in years:
        area_data = get_area_data(region, year)
        if area_data:
            analysis_results.append({'Region': region, 'Year': year, **area_data})
    return analysis_results

def save_analysis_results(analysis_results):
    """
    Saves the area analysis to a CSV file.
    """
    analysis_dir = Path('data/analysis_results')
    analysis_dir.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(analysis_results)
    results_file = analysis_dir / 'area_analysis1.csv'
    df.to_csv(results_file, index=False)
    print(f"✅ Analysis results saved to: {results_file}")

# =================== Main Function ===================

def main():
    # Import analyze_region only when needed
    from scripts.analyze import analyze_region  # Moved inside the function

    regions = ['region_1', 'region_2', 'region_3']
    all_results = []

    for region in regions:
        print(f"🔍 Analyzing {region}...")
        region_results = analyze_region(region)
        all_results.extend(region_results)

    save_analysis_results(all_results)

    # Optional: Trend Prediction (uncomment if needed)
    # from joblib import load
    # model_path = Path("models/trend_predictor.pkl")
    # if model_path.exists():
    #     trend_model = load(model_path)
    #     df_analysis = pd.DataFrame(all_results)
    #     trend_df = predict_trend(df_analysis, trend_model)
    #     trend_df.to_csv('data/analysis_results/future_trend_predictions.csv', index=False)
    #     print("📈 Future trend predictions saved.")
    # else:
    #     print("⚠️ trend_predictor.pkl not found. Skipping future trend prediction.")

# Optional: Add this only if trend prediction is enabled
# def predict_trend(analysis_df, trend_model):
#     predictions = []
#     for region in analysis_df['Region'].unique():
#         df_region = analysis_df[analysis_df['Region'] == region].sort_values('Year')
#         recent = df_region.tail(3)
#         if len(recent) < 3:
#             continue
#         features = recent.iloc[:, 2:].sum(axis=1).values.tolist()
#         if len(features) != 3:
#             continue
#         predicted = trend_model.predict([features])[0]
#         predictions.append({'Region': region, 'Predicted_Area': predicted})
#     return pd.DataFrame(predictions)

if __name__ == "__main__":
    main()
