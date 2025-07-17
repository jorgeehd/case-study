import asyncio
from contextlib import AsyncExitStack
from agents.mcp import MCPServerStdio
from agents import Agent, Runner, ModelSettings
from agents import WebSearchTool
from templates import tutorial_finder_instructions  

# Define MCP server parameters
fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}
playwright_params = {
    "command": "npx",
    "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
}


tutorial_mcp_server_params = [fetch_params, playwright_params]

class TutorialFinderAgent:
    def __init__(self):
        self.name = "tutorialFinder_agent"
    
    async def run_with_mcp_servers(self):
        async with AsyncExitStack() as stack:
            # Start MCP servers
            mcp_servers = [
                await stack.enter_async_context(
                    MCPServerStdio(params, client_session_timeout_seconds=120)
                ) 
                for params in tutorial_mcp_server_params
            ]
            
            
            await self.run_agent(mcp_servers)
    
    async def run_agent(self, mcp_servers):
        # Create agent
        agent = Agent(
            name=self.name,
            instructions=tutorial_finder_instructions(),  # Define this in templates
            model="gpt-4o-mini",
            tools=[WebSearchTool(search_context_size="medium")],
            mcp_servers=mcp_servers,
            model_settings=ModelSettings(
                max_tokens=800,
                tool_choice="required"
            ),
            output_type=str,
        )
        
        # Example query
        query = "How do I install a new dishwasher drain pump from PartsSelect.com?"
        result = await Runner.run(agent, query)
        print(result.final_output)
        
        return result

async def main():
    tutorial_agent = TutorialFinderAgent()
    await tutorial_agent.run_with_mcp_servers()

if __name__ == "__main__":
    asyncio.run(main())