import io
import torch
from PIL import Image
from app.api.v1.ai import config


async def predict_breed(file):
    file_contents = await file.read()
    image = Image.open(io.BytesIO(file_contents))
    transformed_image = config.transformer(image).unsqueeze(0).to(config.device)

    with torch.no_grad():
        outputs = config.model(transformed_image)

        _, predicted = torch.max(outputs, 1)
        predicted_class = config.classes[predicted.item()]

        return predicted_class
