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

Basic usage:
```bash
python face_crop.py --input /path/to/images --output /path/to/output
```

With circular mask:
```bash
python face_crop.py --input /path/to/images --output /path/to/output --circular
```

### Arguments

- `--input`: Input folder path (default: current directory)
- `--output`: Output folder path (default: ./results)
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

基本用法：
```bash
python face_crop.py --input /圖片資料夾路徑 --output /輸出資料夾路徑
```

使用圓形遮罩：
```bash
python face_crop.py --input /圖片資料夾路徑 --output /輸出資料夾路徑 --circular
```

### 參數說明

- `--input`：輸入資料夾路徑（預設：目前資料夾）
- `--output`：輸出資料夾路徑（預設：./results）
- `--circular`：套用圓形遮罩（選用）

## 輸出結果

- 格式：具透明度的 PNG
- 檔名：`[原始檔名]_cropped.png`
- 比例：正方形（1:1）