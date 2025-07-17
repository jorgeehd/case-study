import asyncio
from contextlib import AsyncExitStack
from agents.mcp import MCPServerStdio
from agents import Agent, Runner, ModelSettings
from agents import WebSearchTool
from templates import customer_transaction_instructions

fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}
playwright_params = {
    "command": "npx",
    "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
}

customer_transaction_mcp_server_params = [fetch_params, playwright_params]

class CustomerTransactionAgent:
    def __init__(self):
        self.name = "customer_transaction_agent"
    
    async def run_with_mcp_servers(self, query: str = None):
        async with AsyncExitStack() as stack:
            mcp_servers = [
                await stack.enter_async_context(
                    MCPServerStdio(params, client_session_timeout_seconds=120)
                ) 
                for params in customer_transaction_mcp_server_params
            ]
            await self.run_agent(mcp_servers, query)
    
    async def run_agent(self, mcp_servers, query: str = None):
        agent = Agent(
            name=self.name,
            instructions=customer_transaction_instructions(),
            model="gpt-4o-mini",
            tools=[WebSearchTool(search_context_size="low")],
            mcp_servers=mcp_servers,
            model_settings=ModelSettings(
                max_tokens=800,
                tool_choice="required"
            ),
            output_type=str,
        )

        if query is None:
            query = "My dishwasher isn’t draining — what part might be broken and where can I buy it?"
        
        result = await Runner.run(agent, query)
        print(result.final_output)
        return result

async def main():
    transaction_agent = CustomerTransactionAgent()
    await transaction_agent.run_with_mcp_servers()

if __name__ == "__main__":
    asyncio.run(main())
