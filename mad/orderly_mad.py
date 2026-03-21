from typing import List
import agents.ollama_agent as ag
import numpy as np

def orderly_mad(news_file: str,
                agents: List[ag.Agent],
                max_rounds: int,
                order: str = "round") -> List[ag.Message]:
    # Initialize transcript with the news file
    transcript = [ag.Message(role="user", content=f"News File: {news_file}", author="Moderator")]
    
    # Loops through agents for at most max_rounds times
    for i in range(max_rounds):
        # Determine whose turn it is
        if order == "round":
            current_agent = agents[i % len(agents)]
        elif order == "random":
            current_agent = agents[np.random.randint(0, len(agents))]
        
        # Print who is thinking
        print(f"[* turn ({i + 1}) *] {current_agent.name} is thinking...")
        response = current_agent.respond(transcript)
        
        # Add response to transcript
        transcript.append(response)
            
        # Immediate feedback in terminal
        print(f"[{current_agent.name}]: {response.content}\n")
        
    return transcript