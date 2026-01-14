# Hyperparameter Search Guide

## Overview

This guide explains how to run hyperparameter search for learning rate and batch size, then test the best model on the test set.

## Workflow

1. **Hyperparameter Search** → Tests 6 combinations on validation set
2. **Select Best Model** → Based on validation mAP50
3. **Final Test** → Test best model on test set only

## Step 1: Run Hyperparameter Search

```bash
cd python/question2
python hyperparameter_search.py
```

### What it does:
- Tests 6 combinations:
  - Learning Rate: 0.001, 0.01
  - Batch Size: 2, 4, 8
- Runs full 50 epochs for each (no early stopping)
- Uses **validation set** for evaluation
- Saves results to `hyperparameter_results/validation_metrics.csv`

### Output:
- `hyperparameter_results/validation_metrics.csv` - All validation metrics
- `hyperparameter_results/best_model_info.txt` - Best model information
- `hyperparameter_results/exp_*/` - Individual experiment results

### Expected Time:
- ~6-12 hours (depending on CPU/GPU)
- Each experiment: ~1-2 hours

## Step 2: Review Results

After hyperparameter search completes:

```bash
# View validation metrics
cat hyperparameter_results/validation_metrics.csv
```

The script automatically selects the best model based on validation mAP50.

## Step 3: Final Test on Test Set

```bash
python final_test.py
```

### What it does:
- Loads best model from hyperparameter search
- Tests **only on test set** (never used before)
- Saves final results to `hyperparameter_results/test_results.csv`

### Output:
- `hyperparameter_results/test_results.csv` - Final test metrics

## Results Files

### validation_metrics.csv
Contains validation results for all experiments:
- experiment_id, name, learning_rate, batch_size
- mAP50, mAP50_95, precision, recall
- best_epoch, model_path

### test_results.csv
Contains final test results for best model:
- model_name, learning_rate, batch_size
- validation_mAP50, validation_precision, validation_recall
- test_mAP50, test_mAP50_95, test_precision, test_recall
- model_path

## Important Notes

1. **Validation set** is used for hyperparameter tuning
2. **Test set** is used ONLY for final evaluation
3. No early stopping - all experiments run full 50 epochs
4. Best model selected based on validation mAP50
5. Test set is never used during hyperparameter search

## Troubleshooting

**Out of memory:**
- Reduce batch size in experiments
- Use smaller image size (but keep it fixed across experiments)

**Training too slow:**
- Use GPU if available (change DEVICE in script)
- Reduce number of experiments

**Missing metrics:**
- Check that training completed successfully
- Verify data.yaml paths are correct

