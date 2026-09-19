from PIL import Image
import torch

from torchvision.models import (
    mobilenet_v3_small,
    MobileNet_V3_Small_Weights
)
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

from config import (
    CAPTION_MODEL,
    MAX_IMAGE_SIZE,
    MAX_NEW_TOKENS
)


class ImageAnalyzer:
    """Extract visual evidence from an image."""

    def __init__(self):
        print("Loading image classification model...")

        self.classification_weights = (
            MobileNet_V3_Small_Weights.DEFAULT
        )

        self.classification_model = mobilenet_v3_small(
            weights=self.classification_weights
        )

        self.classification_model.eval()

        print("Loading image captioning model...")

        self.caption_processor = (
            BlipProcessor.from_pretrained(CAPTION_MODEL)
        )

        self.caption_model = (
            BlipForConditionalGeneration.from_pretrained(
                CAPTION_MODEL
            )
        )

        self.caption_model.eval()

        print("Image analyzer ready.")

    def load_image(self, image_path):
        """Load and resize an image."""

        image = Image.open(image_path).convert("RGB")
        image.thumbnail(MAX_IMAGE_SIZE)

        return image

    def classify_image(self, image):
        """Return the top visual classifications."""

        preprocess = self.classification_weights.transforms()
        image_tensor = preprocess(image).unsqueeze(0)

        with torch.no_grad():
            output = self.classification_model(
                image_tensor
            )

        probabilities = torch.softmax(output, dim=1)[0]

        values, indices = torch.topk(
            probabilities,
            k=5
        )

        categories = (
            self.classification_weights.meta["categories"]
        )

        predictions = []

        for value, index in zip(values, indices):
            predictions.append(
                {
                    "label": categories[index],
                    "confidence": float(value)
                }
            )

        return predictions

    def generate_caption(self, image):
        """Generate a natural-language image description."""

        inputs = self.caption_processor(
            images=image,
            return_tensors="pt"
        )

        with torch.no_grad():
            output = self.caption_model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS
            )

        caption = self.caption_processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption.strip()

    def analyze(self, image_path):
        """Perform complete visual analysis."""

        image = self.load_image(image_path)

        classifications = self.classify_image(image)
        caption = self.generate_caption(image)

        return {
            "caption": caption,
            "classifications": classifications,
            "primary_classification": (
                classifications[0]
                if classifications
                else None
            )
        }