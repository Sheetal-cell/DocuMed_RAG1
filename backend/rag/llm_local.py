import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from peft import PeftModel


BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"

ADAPTER_PATH = "models/documed-qwen-lora"


print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    BASE_MODEL
)


print("Loading base Qwen model...")

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True
)

model = model.to("cpu")


print("Loading DocuMed LoRA adapter...")

model = PeftModel.from_pretrained(
    model,
    ADAPTER_PATH
)

model.eval()

print("DocuMed Qwen loaded successfully!")


def generate_answer(prompt):

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    inputs = {
        key: value.to("cpu")
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.2,
            do_sample=True,
            repetition_penalty=1.1
        )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()