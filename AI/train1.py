import torch
from torch import nn
from torch.utils.data import DataLoader

from torchvision import models
from torchvision import transforms


device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)


num_classes = 15

model = models.resnet101(pretrained=True)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, num_classes)
input_size = 224

# 모델을 디바이스로 이동
model.to(device)

# 변경된 모델 확인
print(model)


from torch.utils.data import Dataset
from torchvision import datasets
import matplotlib.pyplot as plt
import os
import pandas as pd
from PIL import Image

classes = os.listdir('images')

train_data = []
test_data = []

for class_name in classes:
  image_lst = os.listdir(f'images/{class_name}')    # class_name이라는 이름을 가진 폴더 내의 사진 이름들의 List 반환
  class_data = [(image, class_name) for image in image_lst]
  rate = int(len(class_data) * 0.8)
  train_data += class_data[:rate]
  test_data += class_data[rate:]
  class_data.clear()

print(len(train_data))
print(len(test_data))

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

class WhatMeowData(Dataset):
    def __init__(self, data, transform,classes):    # __init__ -> class를 선언하자마자 최초로 한 번 실행되는 함수
      self.data = data
      self.transform = transform
      self.classes = classes
    def __len__(self):
      return len(self.data)
    def __getitem__(self, idx):
      image_name, class_name = self.data[idx]
      image = Image.open(f'images/{class_name}/{image_name}')
      try:
        transformed_image = self.transform(image)
        transformed_label = self.classes.index(class_name)
        return transformed_image, transformed_label
      except Exception as e:
        print(e)
        print(image_name)
        print(class_name)

from torch.utils.data import DataLoader

train_dataset = WhatMeowData(train_data,preprocess,classes)
test_dataset = WhatMeowData(test_data,preprocess,classes)

train_dataloader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=16, shuffle=True)

from torch import optim
import torch.nn as nn

num_epochs = 5
params_to_update = model.parameters()
optimizer = optim.SGD(params_to_update, lr=0.001, momentum=0.9)
loss_function = nn.CrossEntropyLoss()

# 학습 및 테스트
from tqdm import tqdm

for epoch in tqdm(range(num_epochs),position=0):
  for inputs,labels in tqdm(train_dataloader,leave=False, position=1):
    # image랑 label device로 보내기
    inputs = inputs.to(device)
    labels = labels.to(device)

    # 이전 batch에서 계산된 가중치를 초기화
    optimizer.zero_grad()

    # forward + back propagation 연산
    outputs = model(inputs)
    train_loss = loss_function(outputs, labels)
    train_loss.backward()
    optimizer.step()


  # 이번 Epoch 학습 결과 테스트
  # 10 Epoch마다 학습 결과 테스트하고 싶으면
  # if epoch != 0 and epoch % 10 == 0:
  size = len(test_dataloader.dataset)
  num_batch = len(test_dataloader)
  print(f"Size : {size}")
  print(f"Num_Batch : {num_batch}")
  correct = 0
  test_loss = 0
  accuracy = []
  model.eval()
  with torch.no_grad():
    for i, data in enumerate(test_dataloader, 0):
      inputs, labels = data
      inputs = inputs.to(device)
      labels = labels.to(device)

      # 결과값 연산
      outputs = model(inputs)
      test_loss += loss_function(outputs, labels).item()
      correct += (outputs.argmax(1) == labels).type(torch.float).sum().item()
  test_loss /= num_batch
  correct /= size

  # 학습 결과 출력
  print('Epoch: %d/%d, Train loss: %.6f, Test loss: %.6f, Accuracy: %.2f' %(epoch+1, num_epochs, train_loss.item(), test_loss, 100*correct))

from PIL import Image
model.eval()

test_image = Image.open('test2.jpg')
transformed_image = preprocess(test_image).unsqueeze(0).to(device)
print("Original Image:")
display(test_image)

print("Transformed Image:")
print(transformed_image)

with torch.no_grad():
    outputs = model(transformed_image)

_, predicted = torch.max(outputs, 1)
predicted_class = classes[predicted.item()]

print("Predicted Class:")
print(predicted_class)

size = len(test_dataloader.dataset)
num_batch = len(test_dataloader)
correct_per_class = {class_name: 0 for class_name in classes}
total_per_class = {class_name: 0 for class_name in classes}

model.eval()
with torch.no_grad():
    for i, data in enumerate(test_dataloader, 0):
        inputs, labels = data
        inputs = inputs.to(device)
        labels = labels.to(device)

        # 결과값 연산
        outputs = model(inputs)
        test_loss += loss_function(outputs, labels).item()

        # 각 클래스별로 정확도 추적
        _, predicted = torch.max(outputs, 1)
        for i in range(len(labels)):
            class_name = classes[labels[i].item()]
            total_per_class[class_name] += 1
            if predicted[i].item() == labels[i].item():
                correct_per_class[class_name] += 1

# 전체 정확도 계산
test_loss /= num_batch
correct = sum(correct_per_class.values())
accuracy = correct / size

# 각 클래스별 정확도 계산
class_accuracies = {class_name: correct_per_class[class_name] / total_per_class[class_name] for class_name in classes}

# 학습 결과 출력
print('Epoch: %d/%d, Train loss: %.6f, Test loss: %.6f, Accuracy: %.2f' %(epoch+1, num_epochs, train_loss.item(), test_loss, 100*accuracy))

# 각 클래스별 정확도 출력
for class_name, class_accuracy in class_accuracies.items():
    print(f'Class: {class_name}, Accuracy: {100 * class_accuracy:.2f}')

torch.save(model.state_dict(),"model_state_dict.pth")
