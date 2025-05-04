from pathlib import Path

def get_regions():
    regions_dir = Path('data/raw')
    return [d.name for d in regions_dir.iterdir() if d.is_dir()]

def get_years(region):
    region_dir = Path(f'data/raw/{region}')
    image_files = list(region_dir.glob('*.tif'))  # Find all TIFF images for this region
    
    years = set()
    for image in image_files:
        year = image.stem.split('_')[-1]  # Assuming image filename ends with the year
        years.add(int(year))
    
    return sorted(years)
