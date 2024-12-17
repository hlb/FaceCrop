# FaceCrop

A Python command-line tool for automatically detecting and cropping portrait photos with transparent backgrounds.

## Features

- Automatic face detection and upper body cropping
- Square output format with transparent background
- Optional circular mask
- Batch processing support
- Multiple input formats support (JPG, JPEG, PNG, WEBP)
- High-quality output preservation
- Complete head visibility ensured
- Centered face composition

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/FaceCrop.git
cd FaceCrop

# Install dependencies
pip install -r requirements.txt
```

## Usage

Process a single image:
```bash
python face_crop.py image.jpg
```

Process a directory of images:
```bash
python face_crop.py input_directory --output output_directory
```

With circular mask:
```bash
python face_crop.py image.jpg --circular
# or for directory
python face_crop.py input_directory --output output_directory --circular
```

### Arguments

- `input`: Input image file or directory path
- `--output`: Output directory path (required for directory input, optional for single file)
- `--circular`: Apply circular mask to the output (optional)

## Output

- Format: PNG with transparency
- Naming: `[original_filename]_cropped.png`
- Aspect ratio: Square (1:1)

---

# FaceCrop 人像裁切工具

自動檢測並裁切人像照片的 Python 命令列工具，支援透明背景輸出。

## 功能特點

- 自動檢測人臉並裁切上半身
- 方形輸出格式，具透明背景
- 可選擇性添加圓形遮罩
- 支援批次處理多張圖片
- 支援多種輸入格式（JPG、JPEG、PNG、WEBP）
- 保持原始圖片品質
- 確保人像頭部完整顯示
- 人臉居中構圖

## 安裝方式

```bash
# 複製專案
git clone https://github.com/yourusername/FaceCrop.git
cd FaceCrop

# 安裝相依套件
pip install -r requirements.txt
```

## 使用方法

處理單張圖片：
```bash
python face_crop.py 圖片.jpg
```

處理整個資料夾：
```bash
python face_crop.py 輸入資料夾 --output 輸出資料夾
```

使用圓形遮罩：
```bash
python face_crop.py 圖片.jpg --circular
# 或是處理資料夾時
python face_crop.py 輸入資料夾 --output 輸出資料夾 --circular
```

### 參數說明

- `input`：輸入圖片或資料夾路徑
- `--output`：輸出資料夾路徑（處理資料夾時必填，處理單張圖片時選填）
- `--circular`：套用圓形遮罩（選用）

## 輸出結果

- 格式：具透明度的 PNG
- 檔名：`[原始檔名]_cropped.png`
- 比例：正方形（1:1）