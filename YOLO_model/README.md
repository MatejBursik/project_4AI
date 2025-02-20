# AI Training

## first_model.onnx (Best)
Trained on the dataset called **hornets_1**.

![confusionmatrix](../runs/detect/train14/confusion_matrix.png)

![F1 curve](../runs/detect/train14/F1_curve.png)

![PR curve](../runs/detect/train14/PR_curve.png)

![results](../runs/detect/train14/results.png)

![validation batch](../runs/detect/train14/val_batch0_pred.jpg)

## second_model.onnx (Worst)
Trained on the dataset called **hornets_2**.

![confusionmatrix](../runs/detect/train15/confusion_matrix.png)

![F1 curve](../runs/detect/train15/F1_curve.png)

![PR curve](../runs/detect/train15/PR_curve.png)

![results](../runs/detect/train15/results.png)

![validation batch](../runs/detect/train15/val_batch0_pred.jpg)

## third_model.onnx
Trained on the dataset called **hornets_1**.

![confusionmatrix](../runs/detect/train43/confusion_matrix.png)

![F1 curve](../runs/detect/train43/F1_curve.png)

![PR curve](../runs/detect/train43/PR_curve.png)

![results](../runs/detect/train43/results.png)

![validation batch](../runs/detect/train43/val_batch0_pred.jpg)

#### Hyper parameter tuning

![fitness](../runs/detect/tune4/tune_fitness.png)

![scatter plots](../runs/detect/tune4/tune_scatter_plots.png)

## Development
If you have a nvidia gpu, try using Cuda cores to accelerate the training of models.

- [cuda cores](https://pytorch.org/get-started/locally/) = `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`
