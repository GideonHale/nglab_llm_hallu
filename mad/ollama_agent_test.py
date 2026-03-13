import agents.ollama_agent as ag
from openai import OpenAI
from roles import role_titles, roles
from orderly_mad import orderly_mad
import presets as ap

def main(role):
    # Define our debaters
    agent1 = ap.joseph
    agent2 = ap.steven
    agent3 = ap.benjamin
    agent4 = ap.christopher
    agent5 = ap.elijah

    print("--- Multi-Agent Debate System ---")
    topic = input("Enter the debate topic: ")
    rounds = int(input("Enter number of turns: "))

    final_transcript = orderly_mad(topic,
                [agent1, agent2, agent3, agent4, agent5],
                rounds,
                order="random")

    print("--- Debate Concluded ---")
    
    # Summarize the debate
    summary = ap.summarizer.respond(final_transcript)

    print("\n--- Summary ---\n", summary.content)
    

if __name__ == "__main__":
    print('Role options: ', ', '.join(role_titles))
    while True:
        # role = input("Enter the role: ")
        role = "parent"
        if role in role_titles:
            break
        print("Invalid role. Please try again.")
    main(role)