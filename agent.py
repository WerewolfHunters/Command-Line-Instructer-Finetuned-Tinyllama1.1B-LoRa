import argparse
import json
import os
import subprocess
import sys
import re
from datetime import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import AutoPeftModelForCausalLM

# --- Configuration ---
# Define the path to the fine-tuned model
# Updated path based on user's feedback
model_path = "./tinyllama_finetuned"
# Define log file path
log_file = 'logs/trace.jsonl'

# --- Helper Functions ---

def log_step(step_name, details):
    """Logs a step with timestamp and details to the trace file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "step": step_name,
        "details": details
    }
    with open(log_file, 'a') as f:
        json.dump(log_entry, f)
        f.write('\n')

def generate_plan(instruction, model, tokenizer):
    """Generates a step-by-step plan using the fine-tuned model."""
    prompt = f"### Instruction:\nGenerate a step-by-step plan for the following task: {instruction}\n\n### Response:\n"
    # Ensure inputs are on the correct device (CUDA if available)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = model.generate(**inputs, max_new_tokens=200, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract the plan from the response
    # Assuming the model's response format is consistent
    plan_start = response.find("### Response:\n")
    if plan_start != -1:
        plan = response[plan_start + len("### Response:\n"):].strip()
        # Split the plan into steps (assuming each step is on a new line or numbered)
        steps = [step.strip() for step in plan.split('\n') if step.strip()]
        return steps
    else:
        return ["Could not generate a plan."]

def is_shell_command(step):
    """Checks if a plan step looks like a shell command."""
    # This is a simple check and can be made more sophisticated
    # We look for common command-line patterns at the beginning of the step
    shell_command_patterns = [
        r"^(sudo\s+)?\w+",  # Starts with an optional sudo followed by a word (command)
        r"^!",             # Starts with ! (Colab magic command for shell)
        r"^pip\s+",        # Starts with pip
        r"^apt-get\s+",    # Starts with apt-get
        r"^git\s+",        # Starts with git
        r"^ls",            # Starts with ls
        r"^cd",            # Starts with cd
        r"^mkdir",         # Starts with mkdir
        r"^rm",            # Starts with rm
        r"^echo",          # Starts with echo
    ]
    for pattern in shell_command_patterns:
        if re.match(pattern, step):
            return True
    return False

def dry_run_command(command):
    """Executes a command in dry-run mode using echo."""
    print(f"Executing in dry-run mode: {command}")
    # Use shell=True for simplicity with potential pipes/redirections,
    # but be cautious with untrusted input if this were a real agent.
    subprocess.run(['echo', command], shell=True)

# --- Main Execution ---

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='CLI Agent that generates and executes a plan based on a natural language instruction.')
    parser.add_argument('instruction', type=str, help='The natural language instruction for the agent.')

    # Parse arguments from the command line
    args = parser.parse_args()
    instruction = args.instruction

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Log the initial instruction
    log_step("Instruction received", instruction)

    print(f"Instruction received: {instruction}")

    # Check for CUDA availability
    if not torch.cuda.is_available():
        print("CUDA is not available. This model requires a GPU for efficient execution.")
        print("Please ensure you have a CUDA-enabled GPU and the necessary drivers/libraries installed.")
        log_step("CUDA not available", "Model requires CUDA-enabled GPU.")
        sys.exit(1)

    # Load the fine-tuned model and tokenizer
    print(f"Loading model from {model_path}...")
    try:
        # Ensure model is loaded on CUDA
        model = AutoPeftModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto", # Use auto to let it decide, but requires CUDA
        )
        merged_model = model.merge_and_unload()
        print(f"Loading tokenizer from {model_path}...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        tokenizer.pad_token = tokenizer.eos_token
        print("Model and tokenizer loaded.")
        log_step("Model loaded", "Fine-tuned model and tokenizer loaded successfully.")

    except Exception as e:
        print(f"Error loading model or tokenizer: {e}")
        print(f"Please ensure the '{model_path}' directory exists and contains the model files.")
        # Add a note about the PEFT warning and potential causes for WinError 193
        print("\nNote: If you encountered a 'WinError 193' or PEFT warnings, please ensure:")
        print("1. You have a compatible CUDA toolkit and drivers installed for your GPU.")
        print("2. You have updated the PEFT library locally (`pip install -U peft`).")
        print("3. The model files in the specified path are not corrupted and have correct permissions.")

        log_step("Model loading failed", f"Error: {e}")
        sys.exit(1) # Exit if model loading fails

    # Generate plan using the instruction and the loaded model.
    print("Generating plan...")
    plan = generate_plan(instruction, merged_model, tokenizer)

    # Log the generated plan
    log_step("Plan generated", plan)

    print("\nGenerated Plan:")
    if plan:
        for i, step in enumerate(plan):
            print(f"{i+1}. {step}")
    else:
        print("Could not generate a plan.")

    # Check if the first step is a shell command and perform dry-run if it is.
    if plan and is_shell_command(plan[0]):
        log_step("Checking first step for shell command", plan[0])
        dry_run_command(plan[0])
        log_step("Dry run executed", plan[0])
    else:
        print("\nFirst step is not a recognized shell command or plan is empty. No dry-run executed.")
        if plan:
            log_step("First step not a shell command", plan[0])
        else:
            log_step("Plan is empty", "No plan generated")

    # Log the completion.
    log_step("Process completed", "Plan generated and processed.")

    print("\nAgent process completed. Check logs/trace.jsonl for details.")