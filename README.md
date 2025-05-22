model - resnet 18 с аугументацией: \
 albu.HorizontalFlip(p=0.5), \
 albu.LongestMaxSize(max_size=INFER_HEIGHT, always_apply=True), \
 albu.PadIfNeeded(min_height=int(INFER_HEIGHT*1.1), min_width=int(INFER_WIDTH*1.1), border_mode=2, always_apply=True), \
 albu.RandomCrop(height=INFER_HEIGHT, width=INFER_WIDTH, always_apply=True) \
![image](https://github.com/user-attachments/assets/665cec27-655d-43f0-9bb8-bedb98da0a0f)

Результат на валидационном датасете: valid: 100%|██████████| 186/186 [00:19<00:00,  9.35it/s, dice_loss - 0.3293, fscore - 0.6708, iou_score - 0.5065]


Данные: https://drive.google.com/drive/folders/1P---58NLcYLQX1sArkG0ea_t2fdKsiFp?usp=drive_link \
 из:  
  - https://theairlab.org/yamaha-offroad-dataset/ 
  - https://www.kaggle.com/datasets/magnumresearchgroup/offroad-terrain-attention-region-images?resource=download 
  - http://rugd.vision/ 
