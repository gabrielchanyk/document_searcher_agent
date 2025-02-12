from crewai import Agent, LLM
# this import helps clean up strings from whitespaces
from textwrap import dedent
from langchain_openai import ChatOpenAI
from crewai_tools import PDFSearchTool, JSONSearchTool
import os


class CustomAgents:
    def __init__(self):
        self.llm = LLM(model="ollama/phi4:latest")

    def pdf_agent(self):
        pdf_folder = "pdfs"  # Folder name containing PDF files
        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
        pdf_tools = [PDFSearchTool(os.path.join(pdf_folder, pdf_file)) for pdf_file in pdf_files]
        
        return Agent(
            role="Senior Information Analyst",
            backstory=dedent(f"""You can find anything in a pdf.  The people need you."""),
            goal=dedent(f"""Uncover any information from pdf files exceptionally well."""),
            verbose=True,
            tools=pdf_tools,
            llm=self.llm,
        )

    #powerpoint agent
    def ppt_agent(self):
        # json_tool = JSONSearchTool("summaries.json")
        return Agent(
            role="PowerPoint Assistant",
            goal="Create PowerPoint presentations",
            backstory=dedent(f"""
                You are an AI assistant specializing in creating PowerPoint presentation template using information from pdf agent. 
                Your task is to analyze the summaries from pdf agent, 
                extract critical insights, and generate relevant charts based on this data. 
                Finally, create a well-structured presentation that includes these charts and any necessary images, 
                ensuring the formatting is professional and visually appealing. 
                Note: only use what is from the pdf agent.
            """),
            verbose=True,
            # tools=[json_tool],
            llm=self.llm,
        )
