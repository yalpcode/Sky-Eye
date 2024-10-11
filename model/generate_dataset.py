import os
import shutil
import glob
import random
from tqdm.auto import tqdm

class GenerateDataset:
    def __init__(self, class_datas_path=["videos_and_photo/0-plane", "videos_and_photo/1-helicopter"], dataset_path="dataset", train_size=0.9):
        self.class_datas_path = class_datas_path
        self.dataset_path = dataset_path
        self.train_size = train_size
        self.classes_name = list(map(lambda x: x.split('-')[-1], self.class_datas_path))

        os.makedirs(dataset_path, exist_ok=True)
        os.makedirs(os.path.join(dataset_path, 'train', 'images'), exist_ok=True)
        os.makedirs(os.path.join(dataset_path, 'train', 'labels'), exist_ok=True)
        os.makedirs(os.path.join(dataset_path, 'val', 'images'), exist_ok=True)
        os.makedirs(os.path.join(dataset_path, 'val', 'labels'), exist_ok=True)

    def __copy_data(self, type_data, data):
        print("Copy", type_data)
        for i, (name, dir) in tqdm(enumerate(data), total=len(data)):
            shutil.copyfile(f'{dir}/images/{name}.jpg',
                            f'{self.dataset_path}/{type_data}/images/{str(i).zfill(6)}.jpg')
            shutil.copyfile(f'{dir}/labels/{name}.txt',
                            f'{self.dataset_path}/{type_data}/labels/{str(i).zfill(6)}.txt')

    def gen(self):
        dataset_names = []
        for class_id, class_path in enumerate(self.class_datas_path):
            path = f'{class_path}/labels/*'
            for path in glob.glob(path):
                *dir, name = path[:-4].split('/')
                dataset_names.append((name, '/'.join(dir[:-1])))

        print(len(dataset_names))


        random.shuffle(dataset_names)
        border_div = int(len(dataset_names) * self.train_size)
        train = dataset_names[:border_div]
        val = dataset_names[border_div:]

        self.__copy_data('train', train)
        self.__copy_data('val', val)

        with open(f'{self.dataset_path}/data.yaml', 'w') as file:
            text = f"""train: ./train/images
val: ./val/images


# Classes

nc: {len(self.class_datas_path)}

names: {self.classes_name}"""
            file.write(text)


generate_dataset = GenerateDataset()
generate_dataset.gen()