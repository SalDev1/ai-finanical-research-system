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

            Your job is to convert the user's financial research question
            into a structured, executable research plan.

            The research plan must:
            1. Identify the overall research objective.
            2. Break the objective into clear, specific research tasks.
            3. Assign an appropriate task type to each task.
            4. Define the information required for each task.
            5. Define the expected output of each task.
            6. Define dependencies between tasks when one task requires
            the output of another task.
            7. Keep tasks focused and independently executable where possible.

            Allowed task types:
            - company_identification
            - financial_data
            - financial_analysis
            - risk_analysis

            Important rules:
            - Do not calculate financial values.
            - Do not invent financial facts.
            - Do not execute tools or APIs.
            - Do not generate Python code.
            - Do not invent task types.
            - Do not specify implementation details.
            - Use only the information provided in the user's question.
            - If information is missing, represent it as a required input rather
            than inventing it.

            Return ONLY valid JSON.
            Do not include markdown, explanations, or additional text.
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
                max_new_tokens=500,
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