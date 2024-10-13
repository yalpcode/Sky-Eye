# -*- coding: utf-8 -*-
# !pip install ultralytics clearml
# !apt-get install p7zip-full
# !cp ./drive/MyDrive/train_dataset_minpromtorg_train_dataset.zip ./
# !7z x -pcifrovoy_proryv_2024_mpt_bpla ./train_dataset_minpromtorg_train_dataset.zip -o./data
# Commented out IPython magic to ensure Python compatibility.
# %env CLEARML_WEB_HOST=https://app.clear.ml
# %env CLEARML_API_HOST=https://api.clear.ml
# %env CLEARML_FILES_HOST=<secret>
# %env CLEARML_API_ACCESS_KEY=<secret>
# %env CLEARML_API_SECRET_KEY=<secret>

# !rm -r datasets/dataset
from ultralytics import YOLO
from clearml import Task

from generator import GenerateDataset

generate_dataset = GenerateDataset(class_datas_path=["./data/photos/0-plane", "./data/photos/1-helicopter"], dataset_path="./dataset")
generate_dataset.gen()

# !mkdir datasets
# !mv ./dataset ./datasets/dataset


task = Task.create(
    project_name="yolov11x-drones",
    task_name="datav2-256-batch",
)

model_variant = "yolov11x"
task.set_parameter("model_variant", model_variant)
task.add_tags(["yolov11x"])

model = YOLO('https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x.pt')

args = dict(
    data="/content/datasets/dataset/data.yaml",
    epochs=30,
    workers=8,
    batch=40,
    augment=True
)
task.connect(args)

results = model.train(**args)

# !cp ./runs ./drive/MyDrive/runs/

