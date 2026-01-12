# Image URL Support - Implementation Summary

## Overview
Enhanced the ComfyUI worker to accept images as URLs in addition to base64 encoded strings. This improves usability and helps avoid RunPod's request size limits for large images.

## Changes Made

### 1. Handler.py Updates

#### Modified `upload_images()` function
- Added URL detection logic (checks for `http://` or `https://` prefix)
- Automatically downloads images from URLs using `requests.get()`
- Maintains backward compatibility with base64 encoded images
- Added timeout (30s) for URL downloads
- Enhanced error handling for download failures

#### Updated validation functions
- Modified validation messages to indicate support for both base64 and URLs
- Updated error messages in `validate_input()` to reflect new capabilities

### 2. Documentation Updates

#### API_USAGE.md
- Updated parameter descriptions to mention URL support
- Added URL examples in the "Image Format" section
- Created new "Example Request with URLs" section
- Updated Python example with both base64 and URL options
- Updated JavaScript example with both base64 and URL options

#### README.md
- Updated `input.images` object documentation
- Added note about image input options (base64 vs URLs)
- Highlighted that URLs are recommended for large images to avoid size limits

### 3. Test Files Created

#### test_input_urls.json
- Example JSON payload using image URLs
- Demonstrates simplified API format with URL inputs

#### example_api_usage.py
- Python script with three test functions:
  - `test_with_urls()` - Demonstrates URL usage
  - `test_with_base64()` - Demonstrates base64 usage
  - `test_mixed_format()` - Demonstrates array format with URLs
- Ready to use with proper endpoint configuration

## Usage Examples

### Simplified Format with URLs
```json
{
  "input": {
    "prompt": "Relight Figure 1 using the brightness map from Figure 2",
    "main_image": "https://example.com/images/main.jpg",
    "reference_image": "https://example.com/images/reference.png",
    "steps": 8,
    "cfg": 1
  }
}
```

### Array Format with URLs
```json
{
  "input": {
    "prompt": "Relight the scene",
    "images": [
      "https://example.com/main.jpg",
      "https://example.com/reference.jpg"
    ],
    "steps": 8
  }
}
```

### Mixed Format (Object Array)
```json
{
  "input": {
    "prompt": "Relight the scene",
    "images": [
      {
        "name": "main_image",
        "image": "https://example.com/main.jpg"
      },
      {
        "name": "reference_image", 
        "image": "data:image/png;base64,iVBORw0KGgo..."
      }
    ]
  }
}
```

## Benefits

1. **Avoids Size Limits**: URLs don't contribute to request payload size, avoiding RunPod's 10MB/20MB limits
2. **Simpler Integration**: No need to encode images to base64 for remote images
3. **Better Performance**: Images can be cached on CDNs and downloaded directly by the worker
4. **Backward Compatible**: All existing base64 workflows continue to work
5. **Flexible**: Can mix URLs and base64 in the same request

## Technical Details

### URL Detection
Images starting with `http://` or `https://` are treated as URLs and downloaded automatically.

### Download Timeout
30 second timeout for image downloads (configurable in code).

### Error Handling
- Download failures are caught and reported with detailed error messages
- Failed downloads don't crash the entire job
- Multiple image uploads continue even if one fails

### Image Processing Flow
1. Input validation checks if image is URL or base64
2. If URL: Download image using `requests.get()`
3. If base64: Decode as before
4. Upload decoded/downloaded bytes to ComfyUI
5. Continue with normal workflow execution

## Testing

To test the new functionality:

1. Update `example_api_usage.py` with your endpoint URL and API key
2. Replace example URLs with actual image URLs
3. Run: `python example_api_usage.py`

Or use `test_input_urls.json` as a template for manual testing.

## Notes

- URLs must be publicly accessible (no authentication required)
- Supports common image formats (PNG, JPEG, WebP, etc.)
- Same 30s timeout as other ComfyUI operations
- Downloaded images are temporarily stored in memory before upload to ComfyUI
