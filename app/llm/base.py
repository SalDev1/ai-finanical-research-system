from abc import ABC, abstractmethod
import os;
from openai import OpenAI

# def set_system_message(main_text):
#    print('salman main_text is : ' , main_text)
#    system_message = f"You are a helpful assistant that summarizes the content of a resume in a concise manner and provide crucial insights. \
#     Summarize yourself with the following resume content given to you : {main_text}. \
#     If no content is given, politely ask the user to upload a resume file. \
#     After summarizing, you are ready to provide your insights on where the candidate is ideal for a specific job role"
#    return system_message;

def openai_fn_call(question : str) : 
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    model='gpt-4o-mini'
    system_prompt = ''
    # Having a list of array messages to be passed to the model. 
    messages = [
        {
            # The system prompt is the instructions for the model to follow
            "role": "system", "content":system_prompt
        },
        {
            # The user prompt is the input from the user
            "role":"user", "content": question
        }
    ]
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content 



class LLMClient(ABC):

    @abstractmethod
    # This helps me generate a research plan based on the user's intent so our application engine understands it. 
    async def generate_research_plan(
        self,
        question: str
    ) -> dict:

        """
        Generate a structured research plan
        from the user's financial question.
        """
        await openai_fn_call(question)
        pass