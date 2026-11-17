import asyncio
from app.llm.hugging_face_client import HuggingFaceLLMClient

async def create_research_plan(): 
    # Using Qwen/Qwen2.5-3B model from hugging face.
    llm_client = HuggingFaceLLMClient()
    response = await llm_client.generate_research_plan("Analyze the Apple Stock in the last 5 years")
    print(f"llm response : {response}")

if __name__ == "__main__":
   asyncio.run(create_research_plan())