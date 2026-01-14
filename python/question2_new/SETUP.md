# Setup Guide for question2_new (Python 3.11)

## Virtual Environment Setup

### 1. Create Virtual Environment (in project root)
```bash
# From project root directory
python -m venv venv_py311
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv_py311\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv_py311\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv_py311/bin/activate
```

### 3. Install Packages
```bash
# From project root
pip install -r requirements_py311.txt
```

### 4. Verify Installation
```bash
python --version  # Should show Python 3.11.x
pip list | findstr ultralytics  # Should show ultralytics >= 8.3.0
```

## Usage

### 1. Prepare Dataset (if not already done)
```bash
cd python/question2_new
python prepare_dataset.py
```

### 2. Train Model
```bash
python train.py
```

### 3. Test Model
```bash
python test.py
```

### 4. Generate Inference Images
```bash
python infer.py
```

## Notes

- Virtual environment is created in project root: `venv_py311/`
- All scripts are in `python/question2_new/`
- Results are saved to `python/question2_new/hyperparameter_results/`
- This setup uses Python 3.11 with latest packages (no version pinning)

