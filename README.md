# 🧠 Command-Line Instruction Agent (LoRA Fine-Tuning)

This project showcases an **end-to-end mini-demo** of fine-tuning a small open-weight language model on a curated dataset of CLI-based Q&A pairs using **LoRA**, and deploying it as a command-line agent that generates executable shell plans.

---

## 🚀 Features

- ✅ 200+ command-line Q&A pairs (Bash, Git, tar/gzip, grep, venv, etc.)
- ✅ LoRA fine-tuning on `TinyLlama-1.1B` using free Google Colab (T4 GPU)
- ✅ `agent.py`: terminal-based agent that:
  - Accepts instructions like `"Create a Git branch"`
  - Generates a shell-based step-by-step plan
  - Performs a dry-run (`echo <command>`)
  - Logs execution to `logs/trace.jsonl`
- ✅ Static & dynamic evaluation with BLEU/ROUGE and plan quality scoring

---

## 🗂️ Project Structure

├── agent.py # CLI agent script<br>
├── data/<br>
│ └── qa_pairs.json # ≥ 150 Q&A pairs for fine-tuning<br>
├── logs/<br>
│ └── trace.jsonl # Dry-run logs from agent<br>
├── lora_adapter/ # LoRA adapter weights after fine-tuning<br>
├── preprocess_data.py # Script to generate dataset<br>
├── finetune_lora_colab.ipynb # Colab notebook for training<br>
├── eval_static.md # Static model evaluation<br>
├── eval_dynamic.md # Dynamic evaluation with scores<br>
├── report.md # One-page project report<br>
└── README.md # This file<br>

---

## 📦 Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/cli-agent-lora.git
cd cli-agent-lora
```

### 2. Set up Environment

```bash
pip install -r requirements.txt
# or install manually:
pip install transformers datasets peft accelerate trl bitsandbytes
```

### 3. Prepare Data

```bash
python preprocess_data.py
```

### 4. Run Fine-Tuning (in Colab)
 - Open and run `finetune_lora_colab.ipynb`. It will:
 - Load the dataset
 - Fine-tune `TinyLlama-1.1B` using LoRA
 - Save the adapter in `lora_adapter/`

---

## 🧪 Run the Agent

```bash
python agent.py "Create a new Git branch and switch to it"
```
 - Output: A step-by-step plan
 - Dry-run any command it generates
 - Logs to: `logs/trace.jsonl`

---

## 📊 Evaluation
 - `eval_static.md`: compares outputs of base vs. fine-tuned model on 5+ test prompts with BLEU/ROUGE-L metrics.
 - `eval_dynamic.md`: live evaluation of agent with 0–2 plan quality scoring.

---

## 📄 Report Highlights
 - Dataset: 200 CLI Q&A pairs from cli-commands-explained(https://huggingface.co/datasets/vaibhav/cli-commands-explained)
 - Model: TinyLlama/TinyLlama-1.1B-Chat(https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
 - Fine-Tuning: 1 epoch with LoRA (8-rank) on Colab T4
 - Time: ~20 minutes training
 - Adapter Size: < 500MB

---

## 📌 Future Improvements
 - Add real shell execution with sandboxing
 - Integrate streaming output with agent UI

---

## 🙌 Credits
Built with ❤️ using Hugging Face Transformers, PEFT, and TRL on Google Colab.
