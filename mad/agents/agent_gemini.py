from dataclasses import dataclass, field
from typing import List, Literal, Dict, Any
from google import genai
from google.genai import types

Role = Literal["user", "model"]

@dataclass
class Message:
    role: Role
    content: str

@dataclass
class Agent:
    name: str
    system_prompt: str
    model: str = "gemini-1.5-flash"
    temperature: float = 0.2
    client: genai.Client = field(default=None)

    def respond(self, context: List[Message]) -> Message:
        """
        context: full conversation so far (without this agent's system prompt)
        returns: this agent's next assistant message
        """
        history = [
            types.Content(role=m.role, parts=[types.Part(text=m.content)])
            for m in context
        ]

        # Gemini handles system prompts in the 'config' parameter
        response = self.client.models.generate_content(
            model=self.model,
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=self.temperature,
            ),
        )

        # messages: List[Dict[str, str]] = [{"role": "system", "content": self.system_prompt}]
        # messages += [{"role": m.role, "content": m.content} for m in context]

        # completion = self.client.chat.completions.create(
        #     model=self.model,
        #     messages=messages,
        #     temperature=self.temperature,
        # )
        # content = completion.choices[0].message.content

        return Message(role="assistant", content=response.text)