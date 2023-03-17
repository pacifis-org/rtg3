import os
from kaggle.api.kaggle_api_extended import KaggleApi


def main():
    # We assume that the kaggle.json file is in the ~/.kaggle directory
    api = KaggleApi()
    api.authenticate()

    dataset_owner = "ioexception"
    dataset_name = "yugioh-cards"
    download_path = os.path.dirname(
        os.path.realpath(__file__)
    )  # directory that this script is in

    api.dataset_download_files(
        f"{dataset_owner}/{dataset_name}", path=download_path, quiet=False, unzip=True
    )


if __name__ == "__main__":
    main()
