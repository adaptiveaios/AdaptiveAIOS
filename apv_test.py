# APV Module Testing Script
# Copyright (C) 2024 AdaptiveAIOS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import torch
from torchvision.models import resnet18
from apv_module import APVModule, compare_apvs  # Import APV module functions

# Initialize the model (using ResNet18 as an example)
model = resnet18(weights="ResNet18_Weights.IMAGENET1K_V1")

# Define layers to track in the APV module
layers_to_track = {
    'layer1': model.layer1,
    'layer2': model.layer2,
    'layer3': model.layer3,
    'layer4': model.layer4
}

# Initialize the APVModule with the model and layers to track
apv_module = APVModule(model, layers_to_track)
apv_module.register_hooks()  # Register hooks to capture layer activations

# Generate a test input and pass it through the model to compute APV
input_data = torch.randn(1, 3, 224, 224)  # Example input tensor
_ = model(input_data)  # Forward pass
apv_vector = apv_module.get_apv()  # Compute APV for the input
print("APV Vector:", apv_vector)

# Example of model stability check
# Set the computed APV as the baseline for this input
baseline_apv = apv_vector

# Run the model again with the same input and get a new APV
_ = model(input_data)
new_apv = apv_module.get_apv()

# Check stability by comparing the new APV with the baseline
is_stable = compare_apvs(new_apv, baseline_apv)
print("Model stability:", "Stable" if is_stable else "Changed")

