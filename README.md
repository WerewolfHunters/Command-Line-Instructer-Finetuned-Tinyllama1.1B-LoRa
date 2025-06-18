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
