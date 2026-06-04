import os
from huggingface_hub import HfApi

def upload():
    token = os.environ.get("HF_TOKEN")
    repo_id = "Sharvan12/LULC-dashboard"
    
    print("Initializing Hugging Face API...")
    api = HfApi(token=token)
    
    print("Uploading images to Hugging Face Space assets...")
    api.upload_folder(
        folder_path="scripts/assets/images",
        path_in_repo="scripts/assets/images",
        repo_id=repo_id,
        repo_type="space"
    )
    print("Upload completed successfully!")

if __name__ == "__main__":
    upload()
