# API Usage Guide

This document describes how to use the Qwen Multi-Lightning API with both simplified and full workflow formats.

## Simplified Input Format (Recommended)

The simplified format allows you to send just the essential parameters without needing to understand ComfyUI's node structure.

### Request Structure

```json
{
  "input": {
    "prompt": "Your text prompt describing the editing task",
    "main_image": "data:image/png;base64,BASE64_ENCODED_IMAGE",
    "reference_image": "data:image/png;base64,BASE64_ENCODED_IMAGE",
    "steps": 8,
    "cfg": 1,
    "seed": 878021536094148
  }
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Text description of the editing task (supports Chinese and English) |
| `main_image` | string | Yes | - | Base64-encoded main subject/scene to be relit |
| `reference_image` | string | Yes | - | Base64-encoded lighting map/reference image |
| `steps` | integer | No | 8 | Number of inference steps (1-50) |
| `cfg` | number | No | 1 | CFG scale for guidance (0-20) |
| `seed` | integer | No | random | Random seed for reproducibility |

### Image Format

**Accepted formats:**
```json
// With data URI prefix (recommended)
"main_image": "data:image/png;base64,iVBORw0KGgo...",
"reference_image": "data:image/jpeg;base64,/9j/4AAQSkZJ..."

// Without prefix (also works)
"main_image": "iVBORw0KGgo...",
"reference_image": "/9j/4AAQSkZJ..."
```

### Example Request

```json
{
  "input": {
    "prompt": "使用图2的亮度贴图对图1重新照明(光源来自前方)",
    "main_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA...",
    "reference_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA...",
    "steps": 8,
    "cfg": 1
  }
}
```

## Full Workflow Format (Advanced)

For advanced users who need custom ComfyUI workflows, you can still send the complete workflow definition.

### Request Structure

```json
{
  "input": {
    "workflow": {
      // Complete ComfyUI workflow JSON
    },
    "images": [
      {
        "name": "image.jpg",
        "image": "base64_data"
      }
    ]
  }
}
```

See [test_input.json](test_input.json) for a complete example.

## Response Format

### Success Response

```json
{
  "images": [
    {
      "filename": "ComfyUI_00001_.png",
      "type": "base64",
      "data": "iVBORw0KGgoAAAANSUhEUgA..."
    }
  ]
}
```

Or with S3 URLs (if configured):

```json
{
  "images": [
    {
      "filename": "ComfyUI_00001_.png",
      "type": "s3_url",
      "data": "https://bucket.s3.amazonaws.com/..."
    }
  ]
}
```

### Error Response

```json
{
  "error": "Error message",
  "details": ["Detailed error information"]
}
```

## Usage Examples

### Python Example

```python
import requests
import base64
import json

# Read and encode images
with open("main_image.jpg", "rb") as f:
    image1_b64 = base64.b64encode(f.read()).decode('utf-8')

with open("reference_image.jpg", "rb") as f:
    image2_b64 = base64.b64encode(f.read()).decode('utf-8')

# Prepare request
payload = {
    "input": {
        "prompt": "使用图2的亮度贴图对图1重新照明(光源来自前方)",
        "main_image": image1_b64,
        "reference_image": image2_b64,
        "steps": 8,
        "cfg": 1
    }
}

# Send request
response = requests.post(
    "YOUR_RUNPOD_ENDPOINT",
    json=payload,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

# Process response
result = response.json()
if "images" in result:
    for img in result["images"]:
        if img["type"] == "base64":
            # Decode and save
            img_data = base64.b64decode(img["data"])
            with open(img["filename"], "wb") as f:
                f.write(img_data)
```

### JavaScript/Node.js Example

```javascript
const fs = require('fs');
const axios = require('axios');

// Read and encode images
const image1 = fs.readFileSync('main_image.jpg', { encoding: 'base64' });
const image2 = fs.readFileSync('reference_image.jpg', { encoding: 'base64' });

// Prepare request
const payload = {
  input: {
    prompt: "使用图2的亮度贴图对图1重新照明(光源来自前方)",
    main_image: image1,
    reference_image: image2,
    steps: 8,
    cfg: 1
  }
};

// Send request
axios.post('YOUR_RUNPOD_ENDPOINT', payload, {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
})
.then(response => {
  const result = response.data;
  if (result.images) {
    result.images.forEach(img => {
      if (img.type === 'base64') {
        const buffer = Buffer.from(img.data, 'base64');
        fs.writeFileSync(img.filename, buffer);
      }
    });
  }
})
.catch(error => {
  console.error('Error:', error.response?.data || error.message);
});
```

## Use Case: AI Image Relighting

This API is specifically designed for **AI-powered image relighting** using the Qwen Image Lightning model.

### How It Works

1. **main_image**: The main subject/scene to be relit
2. **reference_image**: The lighting map/reference
3. **prompt**: Describes the lighting transformation in natural language
4. **Output**: The subject with new lighting applied from the reference image

### Example Prompts

```
English:
"Relight image 1 using the brightness map from image 2 (light source from the front)"
"Apply the lighting from image 2 to the person in image 1"
"Transfer the illumination pattern from image 2 to image 1"

Chinese:
"使用图2的亮度贴图对图1重新照明(光源来自前方)"
"将图2的光照效果应用到图1"
"用图2的照明条件重新渲染图1"
```

## Testing

Test files are provided:
- `test_input_simple.json`: Simplified format example
- `test_input.json`: Full workflow format example

To test locally (if handler supports direct invocation):

```bash
python handler.py < test_input_simple.json
```

## Notes

- The handler automatically builds the ComfyUI workflow when using simplified format
- Simplified format is validated before workflow construction
- Both simplified and full workflow formats are supported
- Use named fields (`main_image`, `reference_image`) for clarity
- Legacy `images` array format is still supported for backward compatibility
