from app.llm.llm_client import LLMClient
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
import torch

class HuggingFaceLLMClient(LLMClient):
    def __init__(self, model_id: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)

        # quantization_config = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_quant_type="nf4",
        #     bnb_4bit_compute_dtype=torch.float16,
        #     bnb_4bit_use_double_quant=True,
        # )

        print("Loading model...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            # quantization_config=quantization_config,
        ).to(self.device)

        print(f"Using device: {self.device}")
        print("Model Downloaded")

    async def generate_research_plan(
        self,
        question: str
    ) -> dict:
        SYSTEM_PROMPT = """
            You are a financial research planner.

            Convert the user's question into a structured research plan.

            Return only JSON.
            Do not calculate financial values.
        """
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )
        # Move inputs to GPU
        inputs = {
            key: value.to("cuda")
            for key, value in inputs.items()
        }

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                do_sample=False,
                use_cache=True,
            )

        response = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True,
        )
        return {
            "question": question,
            "response": response
        }