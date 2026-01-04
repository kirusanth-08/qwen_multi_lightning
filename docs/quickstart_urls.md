# Quick Start: Using Image URLs

This guide shows you how to use image URLs with the Qwen Multi-Lightning API.

## Why Use URLs?

✅ **Avoids size limits**: No need to encode large images to base64  
✅ **Simpler code**: Just pass the URL directly  
✅ **Better for CDNs**: Images can be cached and served quickly  
✅ **Mix formats**: Use URLs and base64 in the same request  

## Basic Usage

### Simplified Format (Recommended)

```json
{
  "input": {
    "prompt": "Relight Figure 1 using the brightness map from Figure 2",
    "main_image": "https://example.com/subject.jpg",
    "reference_image": "https://example.com/lighting.jpg",
    "steps": 8,
    "cfg": 1
  }
}
```

### Array Format

```json
{
  "input": {
    "prompt": "Relight the scene",
    "images": [
      "https://example.com/main.jpg",
      "https://example.com/reference.jpg"
    ]
  }
}
```

## Python Example

```python
import requests

# Your RunPod endpoint
ENDPOINT = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"
API_KEY = "YOUR_API_KEY"

payload = {
    "input": {
        "prompt": "Relight the subject with dramatic lighting",
        "main_image": "https://your-cdn.com/images/subject.jpg",
        "reference_image": "https://your-cdn.com/images/lighting.jpg",
        "steps": 8,
        "cfg": 1
    }
}

response = requests.post(
    ENDPOINT,
    json=payload,
    headers={"Authorization": f"Bearer {API_KEY}"}
)

result = response.json()
print(f"Generated {len(result['output']['images'])} images")
```

## cURL Example

```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "input": {
      "prompt": "Relight the scene",
      "main_image": "https://example.com/main.jpg",
      "reference_image": "https://example.com/reference.jpg",
      "steps": 8
    }
  }'
```

## JavaScript/Node.js Example

```javascript
const axios = require('axios');

const payload = {
  input: {
    prompt: "Relight the subject",
    main_image: "https://example.com/main.jpg",
    reference_image: "https://example.com/reference.jpg",
    steps: 8,
    cfg: 1
  }
};

axios.post('YOUR_ENDPOINT_URL', payload, {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
})
.then(response => {
  console.log('Success!', response.data);
})
.catch(error => {
  console.error('Error:', error.response?.data || error.message);
});
```

## Requirements

- URLs must be publicly accessible (no authentication)
- Supported protocols: `http://` and `https://`
- Common image formats: JPG, PNG, WebP, etc.
- Download timeout: 30 seconds

## Mixing Formats

You can use URLs and base64 in the same request:

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

## Troubleshooting

### Image Download Failed
- Check that the URL is publicly accessible
- Verify the URL returns an image (not HTML)
- Check the image format is supported
- Ensure the server responds within 30 seconds

### URL Not Recognized
- Ensure the URL starts with `http://` or `https://`
- Check there are no extra spaces or characters
- Verify the JSON is properly formatted

### Size Limits
Even with URLs, the generated output images are returned as base64 (unless S3 is configured). For very large outputs, consider:
- Configuring S3 upload (see Configuration Guide)
- Using the `/run` endpoint for async processing
- Reducing output resolution in the workflow

## More Information

- Full API documentation: [API_USAGE.md](../API_USAGE.md)
- Implementation details: [url_support_implementation.md](url_support_implementation.md)
- Example scripts: [example_api_usage.py](../example_api_usage.py)
