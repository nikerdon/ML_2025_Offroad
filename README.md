# Offroad Segmentation Prediction
---
This project aims to predict offroad segmentation using machine learning. An API was developed to serve predictions, and the solution was containerized with Docker for seamless deployment.
The dataset used:
 - Off-Road Terrain Attention Region Images
 - Yamaha-CMU Off-Road Dataset (1348 img)
 - Off-road Autonomous Driving Segmentation Dataset

Data: https://drive.google.com/drive/folders/1P---58NLcYLQX1sArkG0ea_t2fdKsiFp?usp=drive_link \
 used:  
  - https://theairlab.org/yamaha-offroad-dataset/ 
  - https://www.kaggle.com/datasets/magnumresearchgroup/offroad-terrain-attention-region-images?resource=download 
  - http://rugd.vision/

# Preprocessing
---
 - We reduce all images to a single size of 960 x 544 pixels 
 - We bring all the masks to a single appearance: we use white for the road and black for everything else.;
 - We delete inappropriate images (for example, with bad masks, without a road, with a field road, a “good” road, transparent fences, etc.); 
 - Removing mask fragments smaller than the specified threshold (<500 pixels).

# Training and Testing
---
Results:

| Model                  | dice loss | f-score | iou-score |
|------------------------|-----------|---------|-----------|
| resnet18 + Unet        | 0,0232    | 0,9769  | 0,9562    |
| mit_b1 + Unet          | 0,0231    | 0,9770  | 0,9564    |
| efficientnet-b1 + Unet | 0,0224    | 0,9776  | 0,9577    |
| mobileone_S1 + Unet    | 0,0228    | 0,9772  | 0,9570    |
| resnet18 + DPT         | 0,0232    | 0,9769  | 0,9562    |
| mit_b1 + DPT           | 0,0231    | 0,9770  | 0,9564    |
| efficientnet-b1 + DPT  | 0,0224    | 0,9776  | 0,9577    |
| mobileone_S1 + DPT     | 0,0228    | 0,9772  | 0,9570    |


# Best model
---
model - resnet 18 with augmentation: \
 albu.HorizontalFlip(p=0.5), \
 albu.LongestMaxSize(max_size=INFER_HEIGHT, always_apply=True), \
 albu.PadIfNeeded(min_height=int(INFER_HEIGHT*1.1), min_width=int(INFER_WIDTH*1.1), border_mode=2, always_apply=True), \
 albu.RandomCrop(height=INFER_HEIGHT, width=INFER_WIDTH, always_apply=True) \
![image](https://github.com/user-attachments/assets/665cec27-655d-43f0-9bb8-bedb98da0a0f)

The result on the validation dataset: valid: 100%|██████████| 186/186 [00:19<00:00,  9.35it/s, dice_loss - 0.3293, fscore - 0.6708, iou_score - 0.5065]


# Backend and Frontend
---
Backend: python app_api.py
Frontend: streamlit run streamlit_app.py

Step 1: Installing Required Libraries
Ensure you have the necessary libraries installed:  

> pip install fastapi uvicorn pydantic scikit-learn pandas

Note: You may need to upgrade or force a reinstall. If you encounter package conflicts, try these commands:  

> pip install --upgrade --force-reinstall <package>
> pip install -I <package>  # Short for --ignore-installed
> pip install --ignore-installed <package>

Step 2: Run the `app_api.py`


# Team members:
---

Nikita Korenko

Elizabeth Gould

Sofiia Mylnikova

Gibert Elena
