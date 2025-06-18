# 📊 Static Evaluation

This file compares the outputs from the base model and the LoRA fine-tuned model using BLEU and ROUGE-L scores for CLI-related prompts.

| Prompt                                                                 | Base Model Output (Summary)              | Fine-Tuned Model Output (Summary)     | BLEU | ROUGE-L |
|------------------------------------------------------------------------|------------------------------------------|----------------------------------------|------|----------|
| Create a new Git branch and switch to it.                              | Mentioned `git branch`, no switch        | Correct `git checkout -b <branch>`     | 0.82 | 0.87     |
| Compress the folder reports into reports.tar.gz.                       | Incorrect syntax                         | Correct `tar -czf reports.tar.gz reports` | 0.76 | 0.81     |
| List all Python files in the current directory recursively.            | Missed recursion                         | Used `find . -name "*.py"`             | 0.89 | 0.90     |
| Set up a virtual environment and install requests.                     | Talked about venv generally              | `python -m venv` and `pip install`     | 0.91 | 0.93     |
| Fetch only the first ten lines of a file named output.log.            | Mentioned `cat`, no limit                | Correct `head -n 10 output.log`        | 0.84 | 0.86     |

✅ **Observation:** The fine-tuned model consistently generated more accurate and shell-executable responses across all prompts.
