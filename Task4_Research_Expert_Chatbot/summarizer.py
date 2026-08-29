from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL = "google-t5/t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)


def summarize_text(text):
    prompt = "summarize: " + text

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    output = model.generate(
        **inputs,
        max_new_tokens=100,
        min_new_tokens=20,
        do_sample=False
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    text = input("Enter abstract: ")

    print("\nSummary:")
    print(summarize_text(text))