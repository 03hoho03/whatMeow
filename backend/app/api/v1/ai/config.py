import torch
import torch.nn as nn
from torchvision import models, transforms
from ultralytics import YOLO

from app.config import settings


class ResNetModel:
    num_classes = 16
    classes = [
        "도메스틱 숏헤어",
        "뱅갈",
        "브리티시 숏헤어",
        "스핑크스",
        "아메리칸 숏헤어",
        "아메리칸 밥테일",
        "샴",
        "턱시도",
        "랙돌",
        "이집션 마우",
        "버만",
        "아비시니안",
        "메인쿤",
        "러시안 블루",
        "봄베이",
        "페르시안",
    ]
    transformer = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    resnet_model = models.resnet18()
    num_features = resnet_model.fc.in_features
    resnet_model.fc = nn.Linear(num_features, num_classes)
    resnet_model.load_state_dict(torch.load(settings.MODEL_PATH, map_location=torch.device("cpu")))
    resnet_model.eval()


class YOLOv8Model:
    yolo_model = YOLO("yolov8n.pt")


yolo_model = YOLOv8Model()
resnet_model = ResNetModel()
