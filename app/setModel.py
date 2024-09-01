from langchain_community.llms import Ollama

class llm:
    def __init__(self, model):
        self.model = model

    def set_llm(self):
        try:
            llm = Ollama(model=self.model, temperature=0.2)
            return llm
        except:
            print("Unable to Connect to Ollama")
            return "Unable to Connect to Ollama"

