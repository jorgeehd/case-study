import os
#from dotenv import load_dotenv
#import together
from agents import Agent , WebSearchTool, ModelSettings
from templates import * 
from pydantic import BaseModel
from agents import Runner
import asyncio


class isValidQuery(BaseModel):
    reason: str
    "Your reasoning for why this is a valid query."

    is_valid: bool 
    "Is the query valid?"

guardrail_agent = Agent(
   name =  "guardrail_agent",
   instructions=guardrail_instructions(),
   model="gpt-4o-mini",
   tools=[WebSearchTool(search_context_size="low")],
   model_settings=ModelSettings(tool_choice="auto"),
   #max_tokens=10,
   output_type=isValidQuery,
)

async def main():
    result = await Runner.run(guardrail_agent, "What is a lower dishrack wheel")
    print(result.final_output)

# Run the async function
asyncio.run(main())