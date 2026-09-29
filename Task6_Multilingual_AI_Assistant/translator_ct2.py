import ctranslate2
from tokenizers import Tokenizer
from huggingface_hub import snapshot_download


MODEL_REPO = "osa911/nllb-200-distilled-600M-ct2-int8"
TOKENIZER_REPO = "facebook/nllb-200-distilled-600M"


LANGUAGE_CODES = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "te": "tel_Telu",
    "es": "spa_Latn"
}


class MultilingualTranslator:
    def __init__(self):
        model_path = snapshot_download(
            repo_id=MODEL_REPO
        )

        tokenizer_path = snapshot_download(
            repo_id=TOKENIZER_REPO,
            allow_patterns=["tokenizer.json"]
        )

        tokenizer_file = f"{tokenizer_path}\\tokenizer.json"

        self.tokenizer = Tokenizer.from_file(tokenizer_file)

        self.translator = ctranslate2.Translator(
            model_path,
            device="cpu"
        )

    def translate(self, text, source_language, target_language):
        if not text or not text.strip():
            return ""

        if source_language == target_language:
            return text

        if source_language not in LANGUAGE_CODES:
            raise ValueError(
                f"Unsupported source language: {source_language}"
            )

        if target_language not in LANGUAGE_CODES:
            raise ValueError(
                f"Unsupported target language: {target_language}"
            )

        source_code = LANGUAGE_CODES[source_language]
        target_code = LANGUAGE_CODES[target_language]

        encoded = self.tokenizer.encode(text)

        source_tokens = (
            [source_code]
            + encoded.tokens
            + ["</s>"]
        )

        result = self.translator.translate_batch(
            [source_tokens],
            target_prefix=[[target_code]]
        )

        output_tokens = result[0].hypotheses[0]

        if output_tokens and output_tokens[0] == target_code:
            output_tokens = output_tokens[1:]

        output_ids = []

        for token in output_tokens:
            token_id = self.tokenizer.token_to_id(token)

            if token_id is not None:
                output_ids.append(token_id)

        decoded = self.tokenizer.decode(
            output_ids,
            skip_special_tokens=True
        )

        return decoded.strip()