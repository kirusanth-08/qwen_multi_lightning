#!/usr/bin/env bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================================"
echo "worker-comfyui-qwen_multi_lightning: Checking Baked-in Models"
echo "======================================================================"

# Models are baked into the container at /comfyui/models/
MODELS_BASE="/comfyui/models"

# Function to check if a specific file exists
check_file() {
    local file_path=$1
    local file_name=$2
    local required=${3:-false}
    
    if [ -f "$file_path" ]; then
        echo -e "${GREEN}✓${NC} $file_name: Found"
        return 0
    else
        if [ "$required" = true ]; then
            echo -e "${RED}✗${NC} $file_name: NOT FOUND at $file_path"
            return 1
        else
            echo -e "${YELLOW}⚠${NC} $file_name: Not found (optional)"
            return 0
        fi
    fi
}

# Function to check if a directory exists and has files
check_directory() {
    local dir_path=$1
    local dir_name=$2
    local required=${3:-false}
    
    if [ -d "$dir_path" ]; then
        local file_count=$(find "$dir_path" -type f 2>/dev/null | wc -l)
        if [ "$file_count" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} $dir_name: Found $file_count file(s)"
            return 0
        else
            if [ "$required" = true ]; then
                echo -e "${RED}✗${NC} $dir_name: Directory exists but is EMPTY"
                return 1
            else
                echo -e "${YELLOW}⚠${NC} $dir_name: Directory exists but is empty"
                return 0
            fi
        fi
    else
        if [ "$required" = true ]; then
            echo -e "${RED}✗${NC} $dir_name: Directory NOT FOUND at $dir_path"
            return 1
        else
            echo -e "${YELLOW}⚠${NC} $dir_name: Directory not found (optional)"
            return 0
        fi
    fi
}

# Check if models directory exists
if [ ! -d "$MODELS_BASE" ]; then
    echo -e "${RED}ERROR: Models directory not found at $MODELS_BASE${NC}"
    echo "Models should be baked into the container during build."
    exit 1
fi

echo -e "${GREEN}✓${NC} Models directory found at: $MODELS_BASE"
echo ""

# Track overall status
ERRORS=0
WARNINGS=0

echo "Checking required models for Qwen Multi Lightning workflow..."
echo "----------------------------------------------------------------------"

# Check required LoRA models
echo ""
echo "LoRA Models (REQUIRED):"
check_file "$MODELS_BASE/loras/Qwen-Image-Lightning-8steps-V2.0.safetensors" "Qwen-Image-Lightning-8steps-V2.0" true || ((ERRORS++))
check_file "$MODELS_BASE/loras/iclight_sd15_fc.safetensors" "iclight_sd15_fc" true || ((ERRORS++))

# Check required VAE
echo ""
echo "VAE Models (REQUIRED):"
check_file "$MODELS_BASE/vae/qwen_image_vae.safetensors" "qwen_image_vae" true || ((ERRORS++))

# Check required UNET
echo ""
echo "UNET/Diffusion Models (REQUIRED):"
check_file "$MODELS_BASE/unet/Qwen-Image-Edit-2509_fp8_e4m3fn.safetensors" "Qwen-Image-Edit-2509_fp8_e4m3fn" true || ((ERRORS++))

# Check required CLIP
echo ""
echo "CLIP Models (REQUIRED):"
check_file "$MODELS_BASE/clip/qwen_2.5_vl_7b.safetensors" "qwen_2.5_vl_7b" true || ((ERRORS++))

# Check optional directories
echo ""
echo "Optional Model Directories:"
check_directory "$MODELS_BASE/checkpoints" "Checkpoints" false || ((WARNINGS++))
check_directory "$MODELS_BASE/controlnet" "ControlNet" false || ((WARNINGS++))
check_directory "$MODELS_BASE/upscale_models" "Upscale Models" false || ((WARNINGS++))

echo ""
echo "======================================================================"

# Print summary
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo "All required models are baked into the container."
    echo "======================================================================"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Checks completed with $WARNINGS warning(s)${NC}"
    echo "All required models are present. Some optional directories are empty."
    echo "======================================================================"
    exit 0
else
    echo -e "${RED}✗ Checks failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    echo ""
    echo "REQUIRED MODELS MISSING!"
    echo ""
    echo "The following models should be baked into the container:"
    echo "  • LoRAs:"
    echo "    - Qwen-Image-Lightning-8steps-V2.0.safetensors"
    echo "    - iclight_sd15_fc.safetensors"
    echo "  • VAE:"
    echo "    - qwen_image_vae.safetensors"
    echo "  • UNET:"
    echo "    - Qwen-Image-Edit-2509_fp8_e4m3fn.safetensors"
    echo "  • CLIP:"
    echo "    - qwen_2.5_vl_7b.safetensors"
    echo ""
    echo "Please rebuild the Docker image to include all required models."
    echo "======================================================================"
    
    # Allow override with environment variable for testing
    if [ "${SKIP_MODEL_CHECK:-false}" = "true" ]; then
        echo -e "${YELLOW}WARNING: Continuing despite errors (SKIP_MODEL_CHECK=true)${NC}"
        exit 0
    fi
    
    exit 1
fi