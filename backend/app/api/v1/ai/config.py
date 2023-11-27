import torch
import torch.nn as nn
from torchvision import models, transforms

# from app.config import settings

num_classes = 15
classes = [
    "이집션 마우",
    "브리티시 쇼트헤어",
    "아메리칸 밥테일",
    "두색털",
    "러시안블루",
    "아비시니안",
    "버먼",
    "래그돌",
    "아메리칸 쇼트헤어",
    "메인쿤",
    "페르시안",
    "벵갈",
    "샴",
    "봄베이",
    "스핑크스",
]
transformer = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model = models.resnet101()
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, num_classes)
model.load_state_dict(torch.load("model_state_dict.pth", map_location=torch.device("cpu")))
model.eval()
