import logging

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GPT2Config,
    StoppingCriteria,
    TextGenerationPipeline,
)
from transformers.pipelines import text_generation

from config import Config

model = "Kogasa/SCRIPBOZO"


class StopOnNthToken(StoppingCriteria):
    def __init__(self, token_id: int, n: int) -> None:
        self.token_id = token_id
        self.n = n

    def __call__(
        self, input_ids: torch.LongTensor, score: torch.FloatTensor, **kwargs
    ) -> bool:
        num_occurrences = (input_ids == self.token_id).sum().item()
        return num_occurrences >= self.n


class Generator:
    config: Config
    pipeline: TextGenerationPipeline
    log: logging.Logger

    def __init__(self, config: Config) -> None:
        self.config = config
        model, tokenizer, device = self.load(config)
        self.pipeline = self.create_pipeline(model, tokenizer, device)
        self.log = logging.getLogger("Generator")

    @staticmethod
    def load(config: Config) -> (AutoModelForCausalLM, AutoTokenizer, str):
        model_config = GPT2Config.from_pretrained(config.model)
        model_config.update(config.model_config)
        tokenizer = AutoTokenizer.from_pretrained(config.model)
        model = AutoModelForCausalLM.from_pretrained(config.model, config=model_config)
        device = (
            "cuda:0"
            if config.use_gpu_if_available and torch.cuda.is_available()
            else "cpu"
        )
        model.to(device)
        return model, tokenizer, device

    @staticmethod
    def create_pipeline(model, tokenizer, device) -> TextGenerationPipeline:
        return text_generation.TextGenerationPipeline(
            model=model,
            tokenizer=tokenizer,
            device=device,
            stopping_criteria=[StopOnNthToken(198, 2)],
        )

    def generate(self, prompt: str) -> str:
        self.log.info(f"Prompt: {prompt}")

        generated = self.pipeline(prompt)[0]["generated_text"]
        trimmed = self.trim_generated_text(prompt, generated)
        self.log.info(f"Generated: {trimmed}")

        return trimmed

    @staticmethod
    def trim_generated_text(original: str, generated: str) -> str:
        length = len(original) + 1
        return generated[length:].strip()
