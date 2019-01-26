import os
import shutil
from pathlib import Path

from dataset import create_gestures_dataset as pkg


def cleanup_dataset():
    path_to_file = Path(os.path.dirname(os.path.abspath(__file__)))

    dataset_path  = list(path_to_file.glob(pkg.DATASET_FOLDER_NAME))

    if dataset_path:
        shutil.rmtree(dataset_path[0])
        pkg.logger.info("Removing dataset")
    else:
        pkg.logger.info("No dataset to remove")


if __name__ == '__main__':
    cleanup_dataset()