import agent_gpt as ag
from typing import List
from openai import OpenAI

def orderly_mad(topic: str, agents: List[ag.Agent], max_rounds: int) -> List[ag.Message]:
    # Initialize transcript with the debate topic
    transcript = [ag.Message(role="user", content=f"Topic: {topic}", author="Moderator")]
    
    for i in range(max_rounds):
        # Determine whose turn it is using modulo for scalability (works for 2+ agents)
        current_agent = agents[i % len(agents)]
        
        print(f"[*] {current_agent.name} is thinking...")
        response = current_agent.respond(transcript)
        
        transcript.append(response)
        
        # Immediate feedback in terminal
        print(f"[{current_agent.name}]: {response.content}\n")
        
    return transcript

role_titles = ['parent', 'mathematician', 'public administrator']
roles = {
    "parent": [
        "You are a parent who advocates for progressive educational reforms and inclusive community policies.",
        "You are a parent who values traditional curriculum and emphasizes individual accountability and family-centered values."
    ],
    "mathematician": [
        "You are a mathematician who believes in using quantitative models to drive social progress and equitable resource distribution.",
        "You are a mathematician who prioritizes pure logic and the objective application of mathematical principles, wary of social engineering."
    ],
    "public administrator": [
        "You are a public administrator who supports robust government intervention and centralized social programs.",
        "You are a public administrator who advocates for limited government, fiscal conservatism, and decentralized local governance."
    ],
}

def main(role):
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    # Define our debaters
    joseph = ag.Agent(
        name="Joseph",
        system_prompt=roles[role][0],
        client=client
    )
    
    steven = ag.Agent(
        name="Steven",
        system_prompt=roles[role][1],
        client=client
    )

    print("--- Multi-Agent Debate System ---")
    topic = input("Enter the debate topic: ")
    rounds = int(input("Enter number of turns: "))

    final_transcript = orderly_mad(topic, [joseph, steven], rounds)

    # Summarize the debate
    summarizer = ag.Agent(
        name="Summarizer",
        system_prompt="You are a neutral observer. Summarize the debate by analyzing each delineated response and identifying the core arguments.",
        client=client
    )
    summary = summarizer.chat(f"Please briefly summarize the key points of the following debate responses:\n{final_transcript}")
    print("\n--- Summary ---\n", summary)
    
    print("--- Debate Concluded ---")

if __name__ == "__main__":
    print('Role options: ', ', '.join(role_titles))
    while True:
        role = input("Enter the role: ")
        if role in role_titles:
            break
        print("Invalid role. Please try again.")
    main(role)