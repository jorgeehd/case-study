import asyncio
from contextlib import AsyncExitStack
from agents.mcp import MCPServerStdio
from agents import Agent, Runner, ModelSettings
from templates import product_info_instructions



#mcp_params
fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}
playwright_params = {
    "command": "npx",
    "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
}

# group_mcp_servers
product_info_mcp_server_params = [fetch_params, playwright_params]


class ProductInfoAgent:
    def __init__(self):
        self.name = "productInfo_agent"
        self.agent = None 
        self.tool =  None
#        self.query = query
    
    async def create_agent(self, mcp_servers) -> Agent: 

        agent = Agent(
            name=self.name,
            instructions=product_info_instructions(),
            model="gpt-4o-mini",
            mcp_servers=mcp_servers,
            model_settings=ModelSettings(
                max_tokens=500,
                tool_choice="required"
            ),
            output_type=str,
        )
        return agent
    
    async def agent_as_tool(self, mcp_servers): 
        agent = await self.create_agent(self, mcp_servers)
        tool = agent.as_tool( tool_name="product info agent",
            tool_description="Allows for indepth search of the PartsSelect inventory for information regarding products."
        )
        return tool 
    

    async def run_with_mcp_servers(self, query):
        async with AsyncExitStack() as stack:
            # Initialize MCP servers
            mcp_servers = [
                await stack.enter_async_context(
                    MCPServerStdio(params, client_session_timeout_seconds=120)
                ) 
                for params in product_info_mcp_server_params
            ]
            
            # Run the agent with the MCP servers
            await self.run_agent(query, mcp_servers)
    
    async def run_agent(self, query,  mcp_servers):
        # Create the agent with MCP servers
        agent = await self.create_agent(mcp_servers)
    
        
        # Run the query
        #query = f"Im looking for a refrigerator shelf"
        result = await Runner.run(agent, query)
        print(result.final_output)
        
        return result
    


# Usage
async def main():
    
    query = f"Im looking for a refrigerator shelf"

    product_agent = ProductInfoAgent()
    await product_agent.run_with_mcp_servers(query)
#    tmp=  product_agent.agent_as_tool()

if __name__ == "__main__":
    asyncio.run(main())