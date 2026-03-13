from . import agents as ag
from . import roles

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
model1 = "mistral-large:latest"
model2 = "gpt-oss:120b"
model3 = "qwen2.5:72b"

joseph = ag.Agent(
    name="Joseph",
    system_prompt=roles[role][0],
    client=client,
    model=model2
)

steven = ag.Agent(
    name="Steven",
    system_prompt=roles[role][1],
    client=client,
    model=model3
)

benjamin = ag.Agent(
    name="Benjamin",
    system_prompt=roles[role][2],
    client=client,
    model=model2
)

christopher = ag.Agent(
    name="Christopher",
    system_prompt=roles[role][3],
    client=client,
    model=model3
)

elijah = ag.Agent(
    name="Elijah",
    system_prompt=roles[role][4],
    client=client,
    model=model2
)

summarizer = ag.Agent(
    name="Summarizer",
    system_prompt="You are a neutral observer. Summarize the debate by analyzing each delineated response and identifying the core arguments.",
    client=client,
    model=model3
)