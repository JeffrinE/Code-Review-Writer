from langchain_community.llms import Ollama
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage, HumanMessage

llm: Ollama

def set_llm(model):
    try:
        global llm
        llm = Ollama(model=model, temperature=0.2)
    except:
        print("Unable to Connect to Ollama")
        return "Unable to Connect to Ollama"

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

    def generate(self, inputs, llm):
        task_info = self.task.info

        messages = [
            SystemMessage(content=f"you are a {self.role}. {self.backstory}. Your goal is {self.goal}."),
            HumanMessage(
                content=f"{task_info.format(file_content=inputs['file_content'], sequence=inputs['sequence'])}")
        ]

        llm_response = llm.invoke(messages)

        return llm_response

    def edit_generate(self, inputs, llm):
        task_info = self.task.info

        messages = [
            SystemMessage(content=f"you are a {self.role}. {self.backstory}. Your goal is {self.goal}."),
            HumanMessage(
                content=f"{task_info.format(file_content_generated=inputs["file_content_generated"], prompt=inputs['prompt'], memory = inputs['memory'])}")
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
    info="From the following text which is a compiled code from all files from a software project generate a documentation or ReadMe "
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


def main(sequence_list, llm):
    readme_generator: GithubReadMe = GithubReadMe(github_agent, github_agent_task)

    sequence = ""
    for i in sequence_list:
        sequence += f"{i.upper()} + \n"

    result = readme_generator.generate(inputs=
                                       {"file_content": file_content_tool.run("_"),
                                        "sequence": sequence}, llm= llm)

    return result


editor_agent = Agent(
    name="content Editor",
    role="Edit given ReadMe by what is said in the prompt",
    goal="Return content edited according to user's requirements",
    backstory="You are a readme editor. Your job is to edit and return the edited content according to the user prompt "
)

editor_agent_task = Task(
    info="{prompt} in {file_content_generated}."
         "Follow the rules given below: "
         "1. Edit only the section told to be edited."
         "2. do not include any notes or return anything other than the readme content"
         "3. return edited content"
         "memory: {memory}",
    expected_output="A text content in markdown format",
    agent=editor_agent,
    name="Editor Agent Result"
)

def editor_agent_response(file_content_generated, prompt, memory, llm):
    edit_generator: GithubReadMe = GithubReadMe(editor_agent, editor_agent_task)
    result = edit_generator.edit_generate(inputs={"file_content_generated": file_content_generated, "prompt": prompt, "memory": memory}, llm= llm)
    return result