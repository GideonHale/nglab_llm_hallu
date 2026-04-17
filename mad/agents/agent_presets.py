import agents.ollama_agent as ag
from roles import role_titles, roles
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
model1 = "mixtral:8x7b"
model2 = "gpt-oss:120b"
model3 = "qwen2.5:72b"

role = "journalist"

joseph = ag.Agent(
    name="Joseph",
    system_prompt=roles[role][0],
    client=client,
    model=model1
)

steven = ag.Agent(
    name="Steven",
    system_prompt=roles[role][1],
    client=client,
    model=model2
)

benjamin = ag.Agent(
    name="Benjamin",
    system_prompt=roles[role][2],
    client=client,
    model=model3
)

christopher = ag.Agent(
    name="Christopher",
    system_prompt=roles[role][3],
    client=client,
    model=model1
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

judge = ag.Agent(
    name="Judge",
    system_prompt="You are an unbiased judge. Give a verdict (a numerical integer score between completely unreliable at 0 and completely reliable at 5) based on the other agents' responses and that's it.",
    client=client,
    model=model3
)

extractor = ag.Agent(
    name="Extractor",
    system_prompt="You are an unbiased extractor. Find the score from 0 to 5 near the beginning and return only that. Return only the integer from 0 to 5.",
    client=client,
    model=model1
)