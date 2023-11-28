import io
import torch
from PIL import Image
from app.api.v1.ai.config import resnet_model, yolo_model


async def predict_breed(file):
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

        return cat_breeds
    else:
        return False


async def extract_cat_from_image_file(image):
    cat_results = []

    result = yolo_model.yolo_model.predict(image, conf=0.5)
    for i, cls in enumerate(result[0].boxes.cls):
        if int(cls) == 15:
            cat_results.append(result[0].boxes.xyxy[i])

    return cat_results
