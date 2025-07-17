import os
#from dotenv import load_dotenv
#import together
from agents import Agent , WebSearchTool, ModelSettings, OpenAIChatCompletionsModel
from templates import orchestrator_instructions, agents
from pydantic import BaseModel
from agents import Runner
import asyncio
from openai import AsyncOpenAI
#from backend.productInfo_agent import ProductInfoAgent



deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
deepseek_client = AsyncOpenAI(base_url=DEEPSEEK_BASE_URL, api_key=deepseek_api_key)

model = OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=deepseek_client)

'''async def get_agent(mcp_servers, model_name) -> Agent:
    researcher = Agent(
        name="productInfo",
        instructions=productInfo(),
        model=get_model(model_name),
        mcp_servers=mcp_servers,
    )
    return researcher

async def get_agent_tool(mcp_servers, model_name) -> Tool:
    researcher = await get_researcher(mcp_servers, model_name)
    return researcher.as_tool(
            tool_name="productInfo_agent",
            tool_description= "a ParstSelect inventory helper able to look through the partsSelect website to find relevant product information"
        )

class orchestrator:
    def __init__(self, name: str, lastname="Trader", model_name="gpt-4o-mini"):
      self.name = "orchestrator"
      self.agent = '''


orchestrator_agent = Agent(
   name =  "orchestrator-agent",
   instructions=orchestrator_instructions(agents=agents),
   model=model,
   tools=[  ],
   model_settings=ModelSettings(
       max_tokens=1000,
#       tool_choice="auto"
       ),
   output_type=str,
)

async def main():
#    print(Agent.list_models())
    result = await Runner.run(orchestrator_agent, "How can I install part number PS11752778?")
    print(result.final_output)

#  product_agent = ProductInfoAgent()
#    await product_agent.run_with_mcp_servers()


# Run the async function
asyncio.run(main())