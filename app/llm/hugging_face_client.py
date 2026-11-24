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
    )  -> dict:
        SYSTEM_PROMPT = """
            You are a Financial Research Planning Engine.

            Your ONLY responsibility is to convert the user's financial research
            question into a structured research plan that can be validated and
            executed by the application.

            ========================
            1. OUTPUT FORMAT
            ========================

            Return ONLY valid JSON.

            Do NOT return:
            - Markdown
            - Code fences
            - Explanations
            - Comments
            - Natural language outside the JSON
            - Python, SQL, or API calls

            The response MUST follow this structure:

            {
                "research_plan": {
                    "research_objective": "...",
                    "tasks": [...]
                }
            }

            Each task MUST contain:

            - task_id
            - task_type
            - objective
            - inputs
            - expected_output
            - depends_on

            "depends_on" MUST always be an array.
            Use [] when there are no dependencies.

            ========================
            2. ALLOWED TASK TYPES
            ========================

            You may ONLY use:

            - company_identification
            - financial_data
            - financial_analysis
            - risk_analysis

            NEVER invent another task type.

            ========================
            3. TASK DEFINITIONS
            ========================

            company_identification:
            Identify the company.

            Required inputs:
            - company_name

            Possible outputs:
            - company_name
            - cik
            - ticker

            Normally:
            "depends_on": []

            ------------------------

            financial_data:
            Retrieve financial facts for the identified company.

            Required inputs:
            - company
            - metrics
            - period

            Possible outputs:
            - revenue
            - net_income
            - total_assets
            - total_liabilities
            - operating_cash_flow
            - other requested financial facts

            Do NOT calculate financial values.

            If company identification is required, depend on the
            company_identification task.

            ------------------------

            financial_analysis:
            Analyze financial data retrieved by a financial_data task.

            Possible outputs:
            - trend_analysis
            - growth_analysis
            - profitability_analysis
            - margin_analysis
            - key_observations

            MUST depend on the relevant financial_data task.

            Do NOT perform the analysis or include actual financial results
            in the research plan.

            ------------------------

            risk_analysis:
            Analyze financial or business risks using information from
            previous research tasks.

            Possible outputs:
            - identified_risks
            - risk_evidence
            - risk_severity
            - risk_explanation

            MUST depend on the relevant preceding task(s).

            Do NOT invent unsupported facts.

            ========================
            4. DEPENDENCIES
            ========================

            Use "depends_on" to represent task dependencies.

            Rules:

            - Every task MUST contain "depends_on".
            - Use [] when there is no dependency.
            - Every dependency MUST reference an existing task_id.
            - A task MUST NOT depend on itself.
            - Do NOT create circular dependencies.
            - Do NOT duplicate dependencies.
            - Dependencies MUST appear before dependent tasks.
            - If an input references another task, that task MUST also appear
            in depends_on.

            Example:

            task_1 → company_identification
            depends_on: []

            task_2 → financial_data
            depends_on: ["task_1"]

            task_3 → financial_analysis
            depends_on: ["task_2"]

            task_4 → risk_analysis
            depends_on: ["task_3"]

            ========================
            5. INPUTS & OUTPUTS
            ========================

            Every task MUST contain the inputs required for its task type.

            When an input comes from a previous task, reference its task_id.

            Example:

            "inputs": {
                "financial_data": "task_2"
            }

            "depends_on": ["task_2"]

            Do NOT invent missing information.

            Every task MUST define specific expected outputs.

            Expected outputs describe what the task should produce.
            Do NOT include actual financial values or analysis results.

            ========================
            6. FINANCIAL ACCURACY
            ========================

            You are a planning engine, NOT a financial data source.

            Do NOT:
            - invent financial numbers
            - calculate financial values
            - fabricate SEC data
            - fabricate company identifiers
            - fabricate sources
            - fabricate financial facts
            - perform financial analysis

            The application is responsible for data retrieval, calculations,
            validation, persistence, and task execution.

            ========================
            7. PLAN QUALITY
            ========================

            Create only the tasks necessary to answer the user's question.

            Each task must have one clear responsibility.

            Use dependencies only when required.

            Before returning the response, verify:

            - Valid JSON
            - research_plan exists
            - research_objective exists
            - tasks is not empty
            - Every task has a unique task_id
            - Every task has a valid task_type
            - Every task has all required fields
            - Every task has depends_on
            - All dependencies reference existing tasks
            - No self-dependencies
            - No circular dependencies
            - Dependencies appear before dependent tasks
            - No financial values or analysis results are fabricated

            Return ONLY the final JSON.
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
                max_new_tokens=1000,
                do_sample=False,
                use_cache=True,
            )

        response = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True,
        )
        return { "question" : question, "response" : response }