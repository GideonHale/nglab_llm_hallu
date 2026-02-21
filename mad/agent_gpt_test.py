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

def main():
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    # Define our debaters
    joseph = ag.Agent(
        name="Joseph",
        system_prompt="You are a progressive parent. Argue for modern, tech-forward child-rearing.",
        client=client
    )
    
    steven = ag.Agent(
        name="Steven",
        system_prompt="You are a traditional parent. Argue for restricted tech use and old-school discipline.",
        client=client
    )

    print("--- Multi-Agent Debate System ---")
    topic = input("Enter the debate topic: ")
    rounds = int(input("Enter number of turns: "))

    final_transcript = orderly_mad(topic, [joseph, steven], rounds)
    
    print("--- Debate Concluded ---")

if __name__ == "__main__":
    main()
