
# **APV Module for Activation Path Tracking**

The **Activation Path Vector (APV) Module** enhances interpretability and stability monitoring for neural networks, including models like Large Language Models (LLMs) and Convolutional Neural Networks (CNNs). By tracking activation patterns at selected layers, this module condenses each layer's activity into compact vectors called APVs. These APVs provide insights into the model's internal pathways, supporting stability checks, troubleshooting, and adaptive learning.

---

## **Key Features**

- **APV Calculation**: Summarizes activation patterns from tracked layers into concise vectors capturing key statistics like mean, variance, max, and the 75th percentile.
- **Model Stability Check**: Compares new APVs with baseline APVs to ensure the model remains consistent.
- **Adaptive Learning**: Allows deviations from successful APV pathways to guide reinforcement learning.

---

## **Getting Started**

### **Prerequisites**

- **Python 3.8+**
- **PyTorch**: Install via:
  ```bash
  pip install torch
  ```
- **TorchVision**: Install via:
  ```bash
  pip install torchvision
  ```

---

### **Installation**

1. Clone the repository and switch to the `Apv_module_project` branch:
   ```bash
   git clone https://github.com/adaptiveaios/AdaptiveAIOS.git
   cd AdaptiveAIOS
   git checkout Apv_module_project
   ```

2. Navigate to the directory containing the APV module:
   ```bash
   cd APV_Module
   ```

3. Install dependencies:
   ```bash
   pip install torch torchvision
   ```

---

## **Usage**

### **1. Initialize the APV Module**
Define the model and specify which layers to track:
```python
from torchvision.models import resnet18
from apv_module import APVModule

# Load a ResNet18 model
model = resnet18(weights="ResNet18_Weights.IMAGENET1K_V1")

# Specify layers to track
layers_to_track = {
    'layer1': model.layer1,
    'layer2': model.layer2,
    'layer3': model.layer3,
    'layer4': model.layer4
}

# Initialize the APV Module
apv_module = APVModule(model, layers_to_track)
apv_module.register_hooks()
```

---

### **2. Generate APVs**
Run a forward pass to compute the APV:
```python
import torch

# Generate a sample input
input_data = torch.randn(1, 3, 224, 224)

# Perform a forward pass through the model
_ = model(input_data)

# Compute and print the APV
apv_vector = apv_module.get_apv()
print("APV Vector:", apv_vector)
```

---

### **3. Model Stability Check**
Compare APVs to detect deviations:
```python
from apv_module import compare_apvs

# Use the computed APV as the baseline
baseline_apv = apv_vector

# Run the same input again
_ = model(input_data)
new_apv = apv_module.get_apv()

# Check stability
is_stable = compare_apvs(new_apv, baseline_apv)
print("Model stability:", "Stable" if is_stable else "Changed")
```

---

## **API Reference**

### **APVModule Class**
- **`__init__(self, model, layers_to_track)`**: Initializes the module with the specified model and layers.
- **`register_hooks(self)`**: Registers hooks to capture activations during forward passes.
- **`compute_layer_apv(self, activation)`**: Computes APV statistics (mean, variance, max, 75th percentile) for a layer.
- **`get_apv(self)`**: Concatenates APVs across all tracked layers into a single vector.
- **`reset_activations(self)`**: Clears stored activations to avoid carry-over effects.

### **compare_apvs Function**
- **`compare_apvs(new_apv, baseline_apv, tolerance=0.05)`**: Compares two APVs and determines stability within a given tolerance.

---

## **Example Output**
```text
APV Vector: tensor([ 0.123, 0.045, 1.234, 0.567, ... ])
Model stability: Stable
```

---

## **License**
This project is licensed under the **GNU Affero General Public License v3.0**. For more information, see the LICENSE file or visit [GNU’s AGPL page](https://www.gnu.org/licenses/agpl-3.0.html).
