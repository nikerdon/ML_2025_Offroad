'''
Backend for prediction from model. Code modified from example in class. 
Instructions unchanged.

Last edit: 06.04.2025 -- Elizabeth Gould

Проверка работы API (/health)
curl -X GET http://127.0.0.1:5000/health
curl -X GET http://127.0.0.1:5000/stats
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d "{\"Pclass\": 3, \"Age\": 22.0, \"Fare\": 7.2500}"
'''

# import libraries
from fastapi import FastAPI #, Request, HTTPException
import cv2 as cv
import numpy as np
import torch
import segmentation_models_pytorch as smp
import albumentations as albu
import json
from pydantic import BaseModel


app = FastAPI()

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
CLASSES = ["background","road"]
colors_imshow = {
        "background" : np.array([0, 0, 0]),
        "road" : np.array([255, 255, 255]),
    }

# Загрузка модели из файла
model = torch.jit.load(f'bestmodel.pt', map_location=DEVICE)

INFER_WIDTH = 448
INFER_HEIGHT = 256

preprocessing_fn = smp.encoders.get_preprocessing_fn("resnet18", "imagenet")

# Счетчик запросов
request_count = 0

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "OK"}


#---------------------------

def get_test_augmentation():
    test_transform = [albu.LongestMaxSize(max_size=max(INFER_WIDTH, INFER_HEIGHT), p=1.0),
    #albu.SmallestMaxSize(max_size=min(INFER_WIDTH, INFER_HEIGHT), p=1.0),
    albu.PadIfNeeded(min_height=INFER_HEIGHT, min_width=INFER_WIDTH, border_mode=0, p=1.0),
    albu.CenterCrop(height=INFER_HEIGHT, width=INFER_WIDTH, p=1.0)]
    return albu.Compose(test_transform)

def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')

def get_preprocessing(preprocessing_fn):
    _transform = [
        albu.Lambda(image=preprocessing_fn),
        albu.Lambda(image=to_tensor, mask=to_tensor),
    ]
    return albu.Compose(_transform)


def colorize_mask(mask: np.ndarray):
    mask = mask.squeeze()
    colored_mask = np.zeros((*mask.shape, 3), dtype=np.uint8)
    #square_ratios = {}
    for cls_code, cls in enumerate(CLASSES):
        cls_mask = mask == cls_code
        #square_ratios[cls] = cls_mask.sum() / cls_mask.size
        colored_mask += np.multiply.outer(cls_mask, colors_imshow[cls]).astype(np.uint8)

    #colored_mask.transpose()
    return colored_mask#, square_ratios

def get_image(file):
    image = cv.imread(file)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    if image is not None:
        test_transform = get_test_augmentation()
        preprocessing = get_preprocessing(preprocessing_fn)

        sample = test_transform(image=image)
        image = sample["image"]
        sample = preprocessing(image=image)
        image = sample["image"]

    return image

def return_mask(data):
    image = get_image(data)
    #image, gt_mask = plot#self.test_dataset[n]
    #gt_mask = gt_mask.squeeze()
    
    if image is not None:
        x_tensor = torch.from_numpy(image).to(DEVICE).unsqueeze(0)
        pr_mask = model(x_tensor)
        pr_mask = pr_mask.squeeze().cpu().detach().numpy()
    
        label_mask = np.argmax(pr_mask, axis=0)
        #print(label_mask.shape, image.shape, gt_mask.shape)

        return(colorize_mask(label_mask))
        #return({"prediction": colorize_mask(label_mask)})
    else:
        return None


#---------------------------------
class PredictionInput(BaseModel):
    image: list

@app.get("/predict_model")
def predict_model():
    global request_count
    request_count += 1
    best_m = return_mask('img.png')
    cv.imwrite('mask.png', best_m)

'''
@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1
    #python_img = json.loads(input_data["image"])
    #image = np.array(python_img)
    best_m = return_mask(input_data["image"])
    
    # ***** choose image type here ******
    # I start with a numpy array, need in this form: (w,h,3)
    # check the structure of the output image
    # should change in routine colorize_mask

    return {best_m}
'''

# host = 0.0.0.0 for docker, 127.0.0.1 without docker
if __name__ == '__main__':
    import uvicorn
    #uvicorn.run(app, host="0.0.0.0", port=5000)
    uvicorn.run(app, host="127.0.0.1", port=5000)



    #from typing import Annotated

'''from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
'''