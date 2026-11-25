# Evaluation Protocol

Each evaluation should record task ID, judge model and version, prompt version, raw output, parsed output, timestamp, and confidence.

For pairwise experiments, evaluate each pair in the original and reversed response order. Compare the resulting preferences to measure position sensitivity and tie rate.

Report:
- Human majority and adjudicated preferences separately
- Individual annotator labels
- Percentage agreement and appropriate chance-corrected reliability
- AI judge accuracy and Cohen's kappa
- Bootstrap confidence intervals
- Category-level performance
- Limitations and rubric version
