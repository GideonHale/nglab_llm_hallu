import agents.ollama_agent as ag
from openai import OpenAI
from roles import role_titles, roles
from orderly_mad import orderly_mad

def main(role):
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    model = "qwen2.5:72b"

    # Define our debaters
    joseph = ag.Agent(
        name="Joseph",
        system_prompt=roles[role][0],
        client=client,
        model=model
    )
    
    steven = ag.Agent(
        name="Steven",
        system_prompt=roles[role][1],
        client=client,
        model=model
    )

    benjamin = ag.Agent(
        name="Benjamin",
        system_prompt=roles[role][2],
        client=client,
        model=model
    )

    print("--- Multi-Agent Debate System ---")
    topic = input("Enter the debate topic: ")
    rounds = int(input("Enter number of turns: "))

    final_transcript = orderly_mad(topic, [joseph, steven, benjamin], rounds)

    print("--- Debate Concluded ---")
    
    # Summarize the debate
    summarizer = ag.Agent(
        name="Summarizer",
        system_prompt="You are a neutral observer. Summarize the debate by analyzing each delineated response and identifying the core arguments.",
        client=client,
        model=model
    )
    summary = summarizer.respond(final_transcript)

    print("\n--- Summary ---\n", summary.content)
    

if __name__ == "__main__":
    print('Role options: ', ', '.join(role_titles))
    while True:
        role = input("Enter the role: ")
        if role in role_titles:
            break
        print("Invalid role. Please try again.")
    main(role)