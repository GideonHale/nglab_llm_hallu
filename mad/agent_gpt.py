from dataclasses import dataclass, field
from typing import List, Literal, Dict, Any
from openai import OpenAI

Role = Literal["system", "user", "assistant"]

@dataclass
class Message:
    role: Role
    content: str

@dataclass
class Agent:
    name: str
    system_prompt: str
    model: str = "gpt-oss:120b"
    temperature: float = 0.2
    client: Any = field(default_factory=OpenAI)

    def respond(self, context: List[Message]) -> Message:
        """
        context: full conversation so far (without this agent's system prompt)
        returns: this agent's next assistant message
        """
        messages: List[Dict[str, str]] = [{"role": "system", "content": self.system_prompt}]
        messages += [{"role": m.role, "content": self.name + ': ' + m.content} for m in context]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        content = completion.choices[0].message.content
        return Message(role="assistant", content=content)
