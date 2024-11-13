APV Module for Activation Path Tracking
Overview

The Activation Path Vector (APV) Module is designed to enhance interpretability and stability monitoring of neural networks, including Large Language Models (LLMs) and CNNs. By tracking activation patterns at selected layers, this module summarizes each layer’s activation into a compact vector (APV). The APV provides a high-level overview of the model's internal pathways, useful for monitoring stability, troubleshooting, and adaptive learning.
Features

  APV Calculation: Summarizes activation patterns from tracked layers into a concise APV, capturing key statistics.
  Model Stability Check: Compares new APVs against baseline APVs to ensure model consistency over time.
  Adaptive Training: Supports reinforcement learning by allowing deviations from successful APV pathways to guide training.

Getting Started
Prerequisites

  Python 3.8+
  PyTorch
  torchvision (for testing with ResNet or similar models)

Installation

Install PyTorch and torchvision:

pip install torch torchvision

Example Usage

  Initialize the APV Module with a Model: Specify the layers you want to track.
  Register Hooks: Hooks capture activations during the forward pass.
  Compute APVs: Run an input through the model and get the APV.

import torch
from torchvision.models import resnet18

# Load the ResNet18 model for testing
model = resnet18(weights="ResNet18_Weights.IMAGENET1K_V1")

# Specify layers to track
layers_to_track = {
    'layer1': model.layer1,
    'layer2': model.layer2,
    'layer3': model.layer3,
    'layer4': model.layer4
}

# Initialize and set up APV module
apv_module = APVModule(model, layers_to_track)
apv_module.register_hooks()

# Run a sample input through the model to generate APV
input_data = torch.randn(1, 3, 224, 224)
_ = model(input_data)  # Forward pass
apv_vector = apv_module.get_apv()
print("APV Vector:", apv_vector)

  Model Stability Check

You can compare the APV from a current input with a baseline APV to ensure stability.

# Define a baseline APV (previously saved or known stable APV)
baseline_apv = apv_vector

# Generate a new APV and compare
_ = model(input_data)
new_apv = apv_module.get_apv()

# Check if the model is stable
is_stable = compare_apvs(new_apv, baseline_apv)
print("Model stability:", "Stable" if is_stable else "Changed")

API Reference
class APVModule

   __init__(self, model, layers_to_track): Initializes APVModule with a model and specific layers to track.
    register_hooks(self): Registers forward hooks to capture activations.
    compute_layer_apv(self, activation): Computes a summarized APV for a layer.
    get_apv(self): Concatenates APVs across layers for a complete APV vector.
    reset_activations(self): Clears stored activations between inferences.

compare_apvs(new_apv, baseline_apv, tolerance=0.05)

  Compares a new APV with a baseline APV and checks for stability within a given tolerance.
