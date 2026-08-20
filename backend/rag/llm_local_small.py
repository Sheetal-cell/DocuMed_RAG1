import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


print("========================================")
print("Loading local DocuMed LLM")
print("========================================")

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Loading Qwen 0.5B model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
)

model.eval()

print("Local LLM loaded successfully!")


def generate_answer(prompt):

    messages = [
        {
            "role": "system",
            "content": (
                "You are DocuMed, a medical information assistant. "
                "Answer ONLY using the context provided by the user. "
                "Do not use outside knowledge. "
                "If the answer cannot be found in the context, say exactly: "
                "\"I could not find this information in the provided documents.\" "
                "Do not diagnose users. "
                "Do not prescribe medication."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_tokens = outputs[
        0
    ][
        inputs["input_ids"].shape[1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()