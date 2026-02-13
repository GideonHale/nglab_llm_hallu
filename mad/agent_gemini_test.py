import agent_gemini as agent
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()  # Loads .env
api_key = os.getenv('GEMINI_API_KEY')
# client = genai.Client(api_key=api_key)

if __name__=='__main__':
    # something isn't working with the api key
    
    client = genai.Client(
        api_key=api_key
    )
    
    model = 'gemini-1.5-flash'

    a = agent.Agent(
        name="James",
        system_prompt=
            """
                University committee for answering questions about
                historical facts
            """,
        model=model,
        client=client,
    )
    
    m = agent.Message(
        role='user',
        content="""
            Where does the quote We the People of the United States
            of America come from?
        """)
    
    response = a.respond([m]).content
    
    print(f"{a.name}: {response}")
    