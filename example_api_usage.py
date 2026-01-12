"""
Example script demonstrating how to use the API with image URLs
"""
import json
import requests

# RunPod endpoint (replace with your actual endpoint)
ENDPOINT_URL = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"
API_KEY = "YOUR_RUNPOD_API_KEY"

def test_with_urls():
    """Test the API with image URLs"""
    payload = {
        "input": {
            "prompt": "Relight Figure 1 using the brightness map from Figure 2 (light source from the front)",
            "main_image": "https://example.com/images/subject.jpg",
            "reference_image": "https://example.com/images/lighting_reference.jpg",
            "steps": 8,
            "cfg": 1,
            "seed": 452037337342133
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print("Sending request with image URLs...")
    response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print("Success!")
        print(f"Generated {len(result.get('output', {}).get('images', []))} images")
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def test_with_base64():
    """Test the API with base64 encoded images"""
    # Note: You would need to provide actual base64 data
    payload = {
        "input": {
            "prompt": "Relight the subject using the reference lighting",
            "main_image": "data:image/png;base64,iVBORw0KGgo...",  # Your base64 data
            "reference_image": "data:image/png;base64,iVBORw0KGgo...",  # Your base64 data
            "steps": 8,
            "cfg": 1
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print("Sending request with base64 images...")
    response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print("Success!")
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def test_mixed_format():
    """Test with array format (backwards compatible)"""
    payload = {
        "input": {
            "prompt": "Relight the scene",
            "images": [
                "https://example.com/main.jpg",  # First image: main
                "https://example.com/reference.jpg"  # Second image: reference
            ],
            "steps": 8
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print("Sending request with array format...")
    response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print("Success!")
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Testing API with different image input formats")
    print("=" * 60)
    
    # Test with URLs
    print("\n1. Testing with image URLs:")
    print("-" * 60)
    test_with_urls()
    
    # Uncomment to test other formats
    # print("\n2. Testing with base64 images:")
    # print("-" * 60)
    # test_with_base64()
    
    # print("\n3. Testing with array format:")
    # print("-" * 60)
    # test_mixed_format()
