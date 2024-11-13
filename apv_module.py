# APV Module for Activation Path Tracking
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

class APVModule:
    """
    The APVModule class captures and summarizes activation patterns of selected layers
    within a model to generate an Activation Path Vector (APV) for each input. This APV
    provides a high-level summary of the model's inner activations and can be used to
    monitor model stability and support adaptive learning.
    """
    
    def __init__(self, model, layers_to_track):
        """
        Initializes the APV module with a model and specified layers to track.
        
        Parameters:
        - model: The neural network model from which to capture activations.
        - layers_to_track: Dictionary of layer names and layer objects to be tracked for APV.
        """
        self.model = model
        self.layers_to_track = layers_to_track  # Dictionary of layers to track for APV
        self.activations = {}  # Store layer activations during the forward pass

    def register_hooks(self):
        """
        Registers forward hooks on each layer specified in layers_to_track. These hooks
        capture activations during the model's forward pass, storing them in the activations
        dictionary for APV computation.
        """
        for layer_name, layer in self.layers_to_track.items():
            layer.register_forward_hook(self._hook_fn(layer_name))

    def _hook_fn(self, layer_name):
        """
        Inner function to create a hook for capturing activations for a specific layer.
        
        Parameters:
        - layer_name: Name of the layer being hooked to track its activations.
        
        Returns:
        - A hook function that captures and stores the layer's activations.
        """
        def hook(module, input, output):
            self.activations[layer_name] = output.detach()  # Detach to avoid gradient tracking
        return hook

    def compute_layer_apv(self, activation):
        """
        Computes the Activation Path Vector (APV) for a given layer's activations by
        calculating summary statistics (mean, variance, max, 75th percentile).
        
        Parameters:
        - activation: Tensor containing the activations from a layer.
        
        Returns:
        - A tensor containing the summarized APV statistics for the layer.
        """
        mean_activation = activation.mean()
        variance_activation = activation.var()
        max_activation = activation.max()
        percentile_75th = torch.quantile(activation, 0.75)

        # Combine these statistics into a single tensor representing the APV for this layer
        return torch.tensor([mean_activation, variance_activation, max_activation, percentile_75th])

    def get_apv(self):
        """
        Calculates the complete APV for the input by computing APVs for each tracked layer
        and concatenating them into a single vector.
        
        Returns:
        - A concatenated tensor representing the APV across all tracked layers.
        """
        apvs = [self.compute_layer_apv(act) for act in self.activations.values()]
        return torch.cat(apvs)  # Concatenate all layer APVs into one vector

    def reset_activations(self):
        """
        Clears the stored activations between inferences to avoid carry-over effects.
        """
        self.activations = {}

def compare_apvs(new_apv, baseline_apv, tolerance=0.05):
    """
    Compares a new APV with a baseline APV to evaluate model stability.
    
    Parameters:
    - new_apv: The APV generated for a current input.
    - baseline_apv: The baseline APV to compare against.
    - tolerance: The maximum allowed deviation between APVs to be considered stable.
    
    Returns:
    - Boolean value indicating if the model's APV is stable (True) or changed (False).
    """
    deviation = torch.abs(new_apv - baseline_apv)
    max_deviation = deviation.max()
    return max_deviation <= tolerance

