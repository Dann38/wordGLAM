1) Обучить при всех признаках (47),
    - координаты блока ($x_0$, $x_1$, $w$, $y_0$, $y_1$, $h$, ) (6 координат)
    - CNN-шрифты (3 координаты)
    - Регулярки (пунктуация 4, число для блока, индикаторы списка) (6 координат)
    - BERT-word (32 координаты)
    
2) batch=512, 
3) 2 TAGConv (k=1), 
4) balans edges class,
5) batch_norm, 
6) pdf

without lay+
F1 (IoU=0.50):  0.35260116
F1 (IoU=0.95):  0.19075145
mAP@IoU[0.50:0.95] = 0.05090333
0.46676387 (VAL: 0.51718070)

with lay+
F1 (IoU=0.50):  0.50137741
F1 (IoU=0.95):  0.28650138
mAP@IoU[0.50:0.95] = 0.05822880
0.47174437 (VAL: 0.47179636)


| x | loss (val) | f1 (50) | f1 (95) |
|---|------------|---------|---------|
| 1 | 0.4928     | 0.5889  | 0.3790  |
| 2 | 0.4717     | 0.5013  | 0.2865  |
| 3 | 0.4770     | 0.4720  | 0.2857  |
| 4 | 0.4574     | 0.4467  | 0.2805  |
         