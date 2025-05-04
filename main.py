from scripts.preprocess import preprocess_images
from scripts.segment_images import segment_images
from scripts.analyze import analyze_area
from scripts.train_unet import train_model  # originally train_unet()
from scripts.dashboard import create_dashboard

def main():
    print("🔄 Preprocessing images...")
    preprocess_images()

    print("🔄 Segmenting images...")
    segment_images()

    print("📊 Analyzing area...")
    analyze_area()

    print("🧠 Training U-Net model...")
    train_model()

    print("📈 Creating dashboard...")
    create_dashboard()

    print("✅ Pipeline completed successfully.")

if __name__ == '__main__':
    main()
