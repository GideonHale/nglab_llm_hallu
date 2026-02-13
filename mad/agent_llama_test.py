import agent_llama as agent
from openai import OpenAI

def orderly_mad(init_prompt, agents, maxiter=10):
    # run each of the agents in turn on the given prompt
    pass

if __name__=='__main__':
    
    model = 'llama3.2'
    # model = 'gpt-4o'

    local_client = OpenAI(
        base_url="http://localhost:11434/v1",  # Ollama's OpenAI-compatible API
        api_key="ollama"  # Dummy value; Ollama ignores it
    )

    a = agent.Agent(
        name="Joseph",
        system_prompt=
            """
                You are a parent of teenagers. Take a liberal stance.
            """,
        model=model,
        client=local_client,
    )
    b = agent.Agent(
        name="Steven",
        system_prompt=
            """
                You are a parent of small kids. Take a conservative stance.
            """,
        model=model,
        client=local_client,
    )
    
    start_m = agent.Message(
        role='user',
        content="At what age should children be receiving cellphones?")
    
    second_m = agent.Message(
        role='user',
        content="When should children get training on knife ettiquette?")
    
    transcript = [start_m, second_m]

    # this next bit is going to be transplanted into the function orderly_mad() above as soon as
    # I can get the models to respond to each other
    curr_agent = a
    curr_opponent = b
    maxiter = 4
    for i in range(maxiter):
        
        n_message = agent.Message(
            role = 'assistant',
            content = curr_agent.name + ': ' + curr_agent.respond(transcript).content # get response
        )
        transcript.append(n_message) # add to transcript
        
        curr_agent, curr_opponent = curr_opponent, curr_agent # swap
    
    # use this as soon as it's implemented
    # transcript = orderly_mad(start_m, [a, b], maxiter)
    
    for message in transcript:
        # print(f"{message.role}: {message.content}")
        print(message.content)
    