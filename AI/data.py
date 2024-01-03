import pandas as pd
import os
import shutil

# 나이별로 사진 분류
df = pd.read_csv('./archive/data/cats.csv')

# csv 파일의 age열의 값이 Baby인 것을 추출
baby = df['age'] == 'Baby'
baby_df = df[baby]              # dataframe으로 변환
baby_df.to_csv("./baby.csv")

# 위 df에서 id열 선택 후 리스트로 변환
baby_id = baby_df['id']
baby_id_list = baby_id.tolist()

before = "./archive/images"
after = "./archive/baby"
move_files = baby_id_list

# age가 Baby인 사진을 "baby"폴더로 이동
for mf in move_files:
    for image, breeds, _, in os.walk(before):
        for breed in breeds:
            breed_folder = os.path.join(image, breed)
            for _, _, files in os.walk(breed_folder):
                for file in files:
                    file = str(file)
                    mf = str(mf)
                    # breed 폴더 안의 파일명에 "baby_id_list"의 요솟값이 들어있으면 "baby" 폴더로 이동
                    if mf in file:
                        original_path = os.path.join(breed_folder, file)
                        move_path = os.path.join(after, file)
                        shutil.move(original_path, move_path)


# baby 폴더의 사진을 종별로 분류
df = pd.read_csv('./archive/data/baby.csv')

Breed_col = df['breed']
Breed_list_1 = Breed_col.tolist()
Breed_list_2 = set(Breed_list_1)      # 중복 제거
Breed_list = list(Breed_list_2)

# 반복 코드 어떻게 짜는지 모르겠어서 노가다..
Tiger = df['breed'] == 'Tiger'
Tiger_df = df[Tiger]

Tiger_id = Tiger_df['id']
Tiger_id_list = Tiger_id.tolist()

move_files = [str(mf) for mf in Tiger_id_list]
before = "./archive/baby"
after = "./archive/Tiger"

for mf in move_files:
    for filename in os.listdir(before):
        filename = str(filename)
        if mf in filename:
            before_file_path = os.path.join(before, filename)
            shutil.move(before_file_path, after)


# 폴더명 변경
parent_dir = "./archive/baby"

for folder_name in os.listdir(parent_dir):
    folder_path = os.path.join(parent_dir, folder_name)

    if os.path.isdir(folder_path):
        new_folder_name = folder_name + "_baby"
        new_folder_path = os.path.join(parent_dir, new_folder_name)
        os.rename(folder_path, new_folder_path)


parent_dir = "./archive/images"

for folder_name in os.listdir(parent_dir):
    folder_path = os.path.join(parent_dir, folder_name)

    if os.path.isdir(folder_path):
        new_folder_name = folder_name + "_adult"
        new_folder_path = os.path.join(parent_dir, new_folder_name)
        os.rename(folder_path, new_folder_path)
