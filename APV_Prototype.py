from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random
import numpy as np

# Load the model and tokenizer
# Replace "meta-llama/Llama-3.2-1B" with a smaller model like "meta-llama/Llama-2-7b" if necessary.
model_name = "meta-llama/Llama-3.2-1B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to generate random baseline prompts
def generate_random_prompts(num_prompts=100):
    """
    Generates a list of random baseline prompts.
    """
    return [f"Random prompt {i}" for i in range(num_prompts)]

# Function to add variations to baseline prompts
def generate_challenging_prompts(baseline_prompts, variation_strength=0.5):
    """
    Generates variations of baseline prompts by adding a random variation value.
    """
    challenging_prompts = []
    for prompt in baseline_prompts:
        variation = random.uniform(0, variation_strength)
        challenging_prompts.append(f"{prompt} with variation {variation}")
    return challenging_prompts

# Function to calculate Activation Path Vectors (APVs)
def calculate_apv(input_text):
    """
    Tokenizes input text and computes the activation path vector by averaging hidden states.
    """
    inputs = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
        hidden_states = outputs.hidden_states
        apv = torch.cat([hs.mean(dim=1) for hs in hidden_states], dim=-1)
    return apv

# Baseline APV Collection
baseline_prompts = generate_random_prompts(100)
baseline_apvs = [calculate_apv(prompt) for prompt in baseline_prompts]

# Store baseline APVs in a dictionary for easy lookup
baseline_apv_dict = dict(zip(baseline_prompts, baseline_apvs))

# Custom loss function to enforce consistency in APVs
class APVConsistencyLoss(torch.nn.Module):
    def __init__(self, baseline_apvs):
        """
        Initializes the consistency loss function with baseline APVs.
        """
        super(APVConsistencyLoss, self).__init__()
        self.baseline_apvs = baseline_apvs

    def forward(self, predicted_apv, prompt):
        """
        Calculates the mean squared error between predicted and baseline APVs.
        """
        baseline_apv = self.baseline_apvs[prompt]
        return torch.nn.functional.mse_loss(predicted_apv, baseline_apv)

# Generate challenging prompts with variations
challenging_prompts = generate_challenging_prompts(baseline_prompts)

# Define optimizer and consistency loss function
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
consistency_loss_fn = APVConsistencyLoss(baseline_apv_dict)

# Training loop to improve response stability using APV consistency loss
for epoch in range(10):  # Number of training epochs
    for prompt in challenging_prompts:
        # Tokenize input and forward pass
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model(**inputs, output_hidden_states=True)
        hidden_states = outputs.hidden_states
        predicted_apv = torch.cat([hs.mean(dim=1) for hs in hidden_states], dim=-1)

        # Calculate APV consistency loss
        loss = consistency_loss_fn(predicted_apv, prompt.split(' with variation ')[0])

        # Backward pass and optimization step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Print training progress
        print(f"Epoch {epoch}, Prompt: {prompt}, Loss: {loss.item()}")

# Dynamic APV Adjustment and Monitoring
def adjust_apv_targets(new_prompt):
    """
    Dynamically adjusts APV targets for new prompts.
    """
    new_apv = calculate_apv(new_prompt)
    baseline_apv_dict[new_prompt] = new_apv

# Example of real-time monitoring and adjustment
new_prompts = ["New prompt example"]
for new_prompt in new_prompts:
    adjust_apv_targets(new_prompt)
    print(f"Adjusted APV for prompt: {new_prompt}")

