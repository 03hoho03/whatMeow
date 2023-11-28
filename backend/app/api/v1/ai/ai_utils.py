import io
import torch
from collections import defaultdict
from PIL import Image

from app.api.v1.ai.config import resnet_model, yolo_model
from app import model


async def get_feature_from_db(cat_breeds, db):
    cat_breeds_dict = defaultdict(int)
    for breed in cat_breeds:
        cat_breeds_dict[breed] += 1

    to_return_lst = []
    for key, value in cat_breeds_dict.items():
        cat_row = db.query(model.CatFeature).filter_by(cat_breed=key).first()
        to_return_lst.append({key: {"count": value, "feature": cat_row.feature}})

    return to_return_lst


async def predict_breed(file, db):
    file_contents = await file.read()
    image = Image.open(io.BytesIO(file_contents))
    yolo_results = await extract_cat_from_image_file(image)
    if len(yolo_results):
        images = []
        cat_breeds = []
        for result in yolo_results:
            x1, y1, x2, y2 = result.tolist()
            croped_image = image.crop((x1, y1, x2, y2))
            images.append(croped_image)
        for image in images:
            transformed_image = resnet_model.transformer(image).unsqueeze(0).to(resnet_model.device)

            with torch.no_grad():
                outputs = resnet_model.resnet_model(transformed_image)

                _, predicted = torch.max(outputs, 1)
                predicted_class = resnet_model.classes[predicted.item()]

            cat_breeds.append(predicted_class)

        return_lst = await get_feature_from_db(cat_breeds, db)

        return return_lst
    else:
        return False


async def extract_cat_from_image_file(image):
    cat_results = []

    result = yolo_model.yolo_model.predict(image, conf=0.5)
    for i, cls in enumerate(result[0].boxes.cls):
        if int(cls) == 15:
            cat_results.append(result[0].boxes.xyxy[i])

    return cat_results
