from typing import List
import agents.gpt as ag

def orderly_mad(topic: str, agents: List[ag.Agent], max_rounds: int) -> List[ag.Message]:
    # Initialize transcript with the debate topic
    transcript = [ag.Message(role="user", content=f"Topic: {topic}", author="Moderator")]
    
    for i in range(max_rounds):
        # Determine whose turn it is using modulo for scalability (works for 2+ agents)
        current_agent = agents[i % len(agents)]
        
        print(f"[* turn ({i}) *] {current_agent.name} is thinking...")
        response = current_agent.respond(transcript)
        
        transcript.append(response)
        
        # Immediate feedback in terminal
        print(f"[{current_agent.name}]: {response.content}\n")
        
    return transcript