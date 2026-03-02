# Downloaded Datasets

This directory contains datasets for the research project. Data files are not committed to git due to size. Follow the download instructions below.

## Dataset 1: commonsense_qa

### Overview
- **Source**: `huggingface:commonsense_qa`
- **Size**: train=9741, validation=1221, test=1140
- **Format**: HuggingFace Dataset (Arrow on disk)
- **Task**: commonsense_multiple_choice
- **Location**: `datasets/commonsense_qa`

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("commonsense_qa")
dataset.save_to_disk("datasets/commonsense_qa")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/commonsense_qa")
```

### Sample Data
- See `datasets/commonsense_qa/samples/examples.json` for 5 examples per split.

## Dataset 2: hellaswag

### Overview
- **Source**: `huggingface:hellaswag`
- **Size**: train=39905, test=10003, validation=10042
- **Format**: HuggingFace Dataset (Arrow on disk)
- **Task**: commonsense_narrative_completion
- **Location**: `datasets/hellaswag`

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("hellaswag")
dataset.save_to_disk("datasets/hellaswag")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/hellaswag")
```

### Sample Data
- See `datasets/hellaswag/samples/examples.json` for 5 examples per split.

## Dataset 3: winogrande_winogrande_debiased

### Overview
- **Source**: `huggingface:winogrande/winogrande_debiased`
- **Size**: train=9248, test=1767, validation=1267
- **Format**: HuggingFace Dataset (Arrow on disk)
- **Task**: pronoun_coreference_commonsense
- **Location**: `datasets/winogrande_winogrande_debiased`

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("winogrande", "winogrande_debiased")
dataset.save_to_disk("datasets/winogrande_winogrande_debiased")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/winogrande_winogrande_debiased")
```

### Sample Data
- See `datasets/winogrande_winogrande_debiased/samples/examples.json` for 5 examples per split.

## Dataset 4: allenai_ai2_arc_ARC-Challenge

### Overview
- **Source**: `huggingface:allenai/ai2_arc/ARC-Challenge`
- **Size**: train=1119, test=1172, validation=299
- **Format**: HuggingFace Dataset (Arrow on disk)
- **Task**: science_commonsense_qa
- **Location**: `datasets/allenai_ai2_arc_ARC-Challenge`

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("allenai/ai2_arc", "ARC-Challenge")
dataset.save_to_disk("datasets/allenai_ai2_arc_ARC-Challenge")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/allenai_ai2_arc_ARC-Challenge")
```

### Sample Data
- See `datasets/allenai_ai2_arc_ARC-Challenge/samples/examples.json` for 5 examples per split.

## Dataset 5: truthful_qa_multiple_choice

### Overview
- **Source**: `huggingface:truthful_qa/multiple_choice`
- **Size**: validation=817
- **Format**: HuggingFace Dataset (Arrow on disk)
- **Task**: truthfulness_and_reasoning
- **Location**: `datasets/truthful_qa_multiple_choice`

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset
dataset = load_dataset("truthful_qa", "multiple_choice")
dataset.save_to_disk("datasets/truthful_qa_multiple_choice")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/truthful_qa_multiple_choice")
```

### Sample Data
- See `datasets/truthful_qa_multiple_choice/samples/examples.json` for 5 examples per split.

## Notes
- The `datasets/.gitignore` file excludes large data artifacts from git.
- `datasets/dataset_summary.json` contains machine-readable schema/split metadata.