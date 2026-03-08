from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import scrape_tool, search_tool, save_tool  

load_dotenv()

class LeadResponse(BaseModel):
    company: str
    contact_info: str
    email: str
    summary: str
    outreach_message: str
    tools_used: list[str]

class LeadResponseList(BaseModel):
    leads: list[LeadResponse]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = PydanticOutputParser(pydantic_object=LeadResponseList)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a sales enablement assistant.
            1. Use the 'scrape' tool to find exactly 5 local small businesses in Vancouver, British Columbia, from a variety of industries, that might need IT services.
            2. For each company identified by the 'scrape' tool, use the 'search' tool to gather detailed information from DuckDuckGo.
            3. Analyze the searched website content to provide:
                - company: The company name
                - contact_info: Any available contact details
                - summary: A brief qualification based on the scraped website content, focusing on their potential IT needs even if they are not an IT company.
                - email addresses
                - outreach message
                - tools_used: List tools used        

            Do not include extra text beyond the formatted output and the save confirmation message.
            4. Return the output as a list of 5 entries in this format: {format_instructions}
            5. After formatting the list of 5 entries, use the 'save_to_text' tool to send the json format to the text file. 
            6. If the 'save' tool runs, say that you ran it. If you did not run the 'save' tool, say that you could not run it.
            """,
        ),
        ("human", "{query}"),  
        ("placeholder", "{agent_scratchpad}"),  
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [scrape_tool, search_tool, save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

query = "Find and qualify exactly 5 local leads in Vancouver for IT Services. No more than 5 small businesses."

raw_response = agent_executor.invoke({"query": query})

try:
    structured_response = parser.parse(raw_response.get('output'))
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)