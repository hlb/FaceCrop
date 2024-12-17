# Technical Documentation

## Face Detection Pipeline

### Primary Detection: MediaPipe
- Uses MediaPipe Face Detection as primary detection method
- Implements dynamic confidence thresholds
- Optimized for both performance and accuracy

### Fallback Detection: Haar Cascade
- Frontal face detection with adaptive scale factors
- Configurable detection parameters
- Enhanced with histogram equalization

### Profile Face Detection
- Specialized detection for side-facing portraits
- Automatic mirror detection for both left and right profiles
- Optimized for profile face characteristics

## Cropping Algorithm

### Face Framing
- Dynamic output size based on detected face dimensions
- Automatic head margin calculation
- Square aspect ratio preservation
- Face-centered composition

### Image Processing
- Multi-stage preprocessing pipeline
- Contrast enhancement techniques
- Transparent background generation
- Anti-aliased circular mask option

## Implementation Details

### Input Processing
- Supported formats: JPG, JPEG, PNG, WEBP
- Quality preservation system
- Automatic format handling

### Output Generation
- PNG format with alpha channel
- Transparent background processing
- Optional circular mask with anti-aliasing
- Standardized output naming convention

### Batch Processing
- Efficient directory traversal
- Progress tracking system
- Detailed success/failure reporting
- Parallel processing capabilities
