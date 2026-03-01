from agents import Agent
from src.core.factory.llm_factory import InitLLM

class BaseAgent(Agent):
  """
  Specialization of the OpenAI Agent class.
  Automatically injects the project's LLM configuration.
  """
  def __init__(self, **kwargs):
    # Automatically inject our LLM factory configuration
    if 'model' not in kwargs:
      kwargs['model'] = InitLLM.configure()
    
    # Forward to the original Agent from the library (keeps Hints and Docs)
    super().__init__(**kwargs)