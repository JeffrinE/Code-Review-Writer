from langchain_community.llms import Ollama
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage, HumanMessage

llm: Ollama
def set_llm():
    try:
        global llm
        llm = Ollama(model='llama3', temperature=0.2)
    except:
        print("Unable to Connect to Ollama or Model: llama3 unavailable")
        return "Unable to Connect to Ollama or Model: llama3 unavailable"

def file_content_function(_):
    with open("output/file_content.txt", "r") as file:
        file_content = file.read()
    return file_content


file_content_tool = Tool.from_function(
    name="File Content Tool",
    description="Provides compiled contents of code files in a project folder.",
    func=file_content_function
)


class Agent:
    def __init__(self, name, role, goal, backstory):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory


class Task:
    def __init__(self, info, expected_output, agent, name):
        self.info = info
        self.expected_output = expected_output
        self.agent = agent
        self.name = name


class GithubReadMe:
    def __init__(self, agent, task):
        self.name = agent.name
        self.role = agent.role
        self.goal = agent.goal
        self.backstory = agent.backstory
        self.task = task

    def generate(self, inputs):
        task_info = self.task.info

        messages = [
            SystemMessage(content=f"you are a {self.role}. {self.backstory}. Your goal is {self.goal}."),
            HumanMessage(
                content=f"{task_info.format(file_content=inputs['file_content'], sequence=inputs['sequence'])}")
        ]

        llm_response = llm.invoke(messages)

        return llm_response


github_agent = Agent(
    name="Github Readme Writer",
    role="Github ReadMe section writer",
    goal="Generate a ReadMe section for the project",
    backstory="You understand a projects code that is compiled into a single text file and generate a ReadMe content."
)

github_agent_task = Task(
    info="From the following text which is a compiled code from all files from a software project generate a ReadMe "
         "content in markdown format, {file_content}."
         "1. Generate the ReadMe content in the following sequence, "
         "{sequence}"
         "2. Ensure to use styling in the markdown"
         "3. Write at least three to five lines for each sequence"
         "4. do not include any notes or return anything other than the readme content",
    expected_output="A text content in markdown format",
    agent=github_agent,
    name="Agent Result"
)


def main(sequence_list):
    readme_generator: GithubReadMe = GithubReadMe(github_agent, github_agent_task)

    sequence = ""
    for i in sequence_list:
        sequence += f"{i.upper()} + \n"

    result = readme_generator.generate(inputs=
                                       {"file_content": file_content_tool.run("_"),
                                        "sequence": sequence})

    return result



