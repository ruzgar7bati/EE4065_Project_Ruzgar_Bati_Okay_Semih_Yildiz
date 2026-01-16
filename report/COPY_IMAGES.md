# Image Files to Copy

Please copy the following image files from their source locations to `report/images/`:

## Question 1 Images

1. **Reference and Python Results:**
   - Source: `python/question1_images/reference_taken_from_phone.jpg`
   - Destination: `report/images/q1_reference_taken_from_phone.jpg`

   - Source: `python/question1_images/figure_grayscale_versus_binaryoutput.png`
   - Destination: `report/images/q1_figure_grayscale_versus_binaryoutput.png`

2. **ESP32 Binary Result:**
   - Source: `python/question1_images/binary.png`
   - Destination: `report/images/q1_binary.png`

3. **Question 3 Python Comparison:**
   - Source: `python/question1_images/q3_comparison.png`
   - Destination: `report/images/q3_comparison.png`

## Question 3 ESP32 Images

1. **ESP32-CAM Results:**
   - Source: `resized-n.jpg` (original 160×120)
   - Destination: `report/images/q3_original.jpg`
   
   - Source: `resized-upsampled.jpg` (upsampled 240×180)
   - Destination: `report/images/q3_upsampled.jpg`
   
   - Source: `resized-downsampled.jpg` (downsampled 106×80)
   - Destination: `report/images/q3_downsampled.jpg`

## Question 2 Images

1. **Test Set Detection Results:**
   - Source: `python/question2_new/figures/result_0_6.png`
   - Destination: `report/images/q2_result_0_6.png`
   
   - Source: `python/question2_new/figures/result_4_6_aug1_rotate.png`
   - Destination: `report/images/q2_result_4_6_aug1_rotate.png`
   
   - Source: `python/question2_new/figures/result_7_6_aug2_contrast.png`
   - Destination: `report/images/q2_result_7_6_aug2_contrast.png`

2. **Validation Batch:**
   - Source: `python/question2_new/hyperparameter_results/exp_3_lr0.001_batch8/val_batch0_labels.jpg`
   - Destination: `report/images/q2_val_batch0_labels.jpg`

3. **Training Results:**
   - Source: `python/question2_new/hyperparameter_results/exp_3_lr0.001_batch8/results.png`
   - Destination: `report/images/q2_training_results.png`

4. **Evaluation Curves:**
   - Source: `python/question2_new/hyperparameter_results/exp_3_lr0.001_batch8/BoxPR_curve.png`
   - Destination: `report/images/q2_box_pr_curve.png`
   
   - Source: `python/question2_new/hyperparameter_results/exp_3_lr0.001_batch8/BoxF1_curve.png`
   - Destination: `report/images/q2_box_f1_curve.png`

## Copy Commands (Windows PowerShell)

```powershell
# Create images directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "report\images"

# Question 1 images
Copy-Item "python\question1_images\reference_taken_from_phone.jpg" "report\images\q1_reference_taken_from_phone.jpg"
Copy-Item "python\question1_images\figure_grayscale_versus_binaryoutput.png" "report\images\q1_figure_grayscale_versus_binaryoutput.png"
Copy-Item "python\question1_images\binary.png" "report\images\q1_binary.png"
Copy-Item "python\question1_images\q3_comparison.png" "report\images\q3_comparison.png"

# Question 3 - ESP32-CAM results
Copy-Item "resized-n.jpg" "report\images\q3_original.jpg"
Copy-Item "resized-upsampled.jpg" "report\images\q3_upsampled.jpg"
Copy-Item "resized-downsampled.jpg" "report\images\q3_downsampled.jpg"

# Question 2 - test set detection results
Copy-Item "python\question2_new\figures\result_0_6.png" "report\images\q2_result_0_6.png"
Copy-Item "python\question2_new\figures\result_4_6_aug1_rotate.png" "report\images\q2_result_4_6_aug1_rotate.png"
Copy-Item "python\question2_new\figures\result_7_6_aug2_contrast.png" "report\images\q2_result_7_6_aug2_contrast.png"

# Question 2 - validation batch
Copy-Item "python\question2_new\hyperparameter_results\exp_3_lr0.001_batch8\val_batch0_labels.jpg" "report\images\q2_val_batch0_labels.jpg"

# Question 2 - training results
Copy-Item "python\question2_new\hyperparameter_results\exp_3_lr0.001_batch8\results.png" "report\images\q2_training_results.png"

# Question 2 - evaluation curves
Copy-Item "python\question2_new\hyperparameter_results\exp_3_lr0.001_batch8\BoxPR_curve.png" "report\images\q2_box_pr_curve.png"
Copy-Item "python\question2_new\hyperparameter_results\exp_3_lr0.001_batch8\BoxF1_curve.png" "report\images\q2_box_f1_curve.png"
```

## Note

All image paths in the LaTeX files assume these files are in `report/images/` with the names specified above.

