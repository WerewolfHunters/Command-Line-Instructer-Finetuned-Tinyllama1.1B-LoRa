# 📝 Project Report: CLI Instruction Agent via LoRA Fine-Tuning

## 📚 Data Sources

We used the [cli-commands-explained](https://huggingface.co/datasets/vaibhav/cli-commands-explained) dataset from Hugging Face, containing curated command-line questions and answers. Each sample includes a `code` (command) and a `description`. After cleaning and deduplication, **200 high-quality Q&A pairs** across topics like Git, Bash, tar/gzip, grep, and venv were used for training.

---

## 🧠 Model & Fine-Tuning

- **Base Model:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
- **Fine-Tuning Technique:** LoRA via Hugging Face PEFT & TRL
- **LoRA Config:** Rank = 8, Alpha = 16, Dropout = 0.1
- **Training Setup:**
  - Platform: Google Colab (T4 GPU)
  - Epochs: 1
  - Optimizer: AdamW
  - Batch Size: 4
  - Max Sequence Length: 512
- **Output:** Adapter weights saved to `lora_adapter/` (≈ 390 MB)

---

## ⚙️ Agent Functionality

- Script: `agent.py`
- Accepts a natural-language CLI task (e.g., "Create a new Git branch and switch to it.")
- Generates a **step-by-step shell plan** using the fine-tuned model
- If the first line is a command, executes it in **dry-run mode** using `echo`
- Logs each step in `logs/trace.jsonl` for traceability

---

## 📊 Evaluation Summary

### Static Evaluation:
- Compared base vs. fine-tuned outputs on 5 prompts
- Metrics: BLEU and ROUGE-L improved by **~15-25%** post fine-tuning
- Fine-tuned model consistently provided **accurate and structured** shell command plans

### Dynamic Evaluation:
- Agent was run live on the same 5 prompts
- Plan quality scored between 0–2
- All responses scored **2/2**, and dry-run logic worked flawlessly

---

## 💡 Improvements & Future Work

1. **Real Command Execution:** Replace dry-run with secure, sandboxed execution for trusted users.
2. **Web Search Integration:** Enhance planning quality using Retrieval-Augmented Generation (RAG) with command-line documentation or Stack Overflow.

---

## 🕒 Training Time & Resources

- Training Duration: ~20 minutes on Colab T4
- RAM Used: ~10 GB
- Disk Used: ~390 MB (adapter only)

---

✅ This project demonstrates how lightweight fine-tuning (LoRA) on small open models can yield reliable task-specific agents, even with limited compute.
