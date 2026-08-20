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
    dtype=torch.float32
)

model.eval()

print("Local LLM loaded successfully!")


def generate_answer(prompt):

    messages = [
        {
            "role": "system",
            "content": (
                "You are DocuMed, a medical information assistant.\n\n"

                "STRICT RULES:\n"
                "1. Answer ONLY from the medical context provided by the user.\n"
                "2. Do not use outside knowledge.\n"
                "3. Do not invent, assume, or add medical facts.\n"
                "4. Answer the exact question asked.\n"
                "5. Keep the answer concise and easy to understand.\n"
                "6. Include the source and page when the context provides them.\n"
                "7. Do not diagnose.\n"
                "8. Do not prescribe medicines or dosages.\n"
                "9. Do not make personalized treatment decisions.\n"
                "10. If the information is not present in the context, respond exactly:\n"
                "\"I could not find this information in the provided documents.\"\n"
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
            max_new_tokens=180,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()