import os
from groq import Groq
from dotenv import load_dotenv
from ..protocols.acp import AgentMessage

load_dotenv()

class LibrarianAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # This is the "Semantic Catalog" - the LLM only sees this, not the whole DB.
        self.catalog = """
        TABLE: customers (columns: id, name, email, join_date)
        TABLE: orders (columns: id, customer_id, order_date, total_amount)
        TABLE: products (columns: id, product_name, price)
        """

    def process_request(self, message: AgentMessage) -> AgentMessage:
        user_query = message.content.get("query")
        
        prompt = f"""
        You are a Data Librarian. Given the following tables:
        {self.catalog}
        
        User Query: "{user_query}"
        
        Identify ONLY the tables needed to answer the query. 
        Output ONLY a comma-separated list of table names.
        Example Output: customers, orders
        
        If the query is dangerous or irrelevant to these tables, output 'REJECT'.
        Do not provide any explanation or extra text.
        """

        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )

        response_content = chat_completion.choices[0].message.content
        
        return AgentMessage(
            sender="LibrarianAgent",
            receiver="Orchestrator",
            performative="INFORM" if "REJECT" not in response_content else "FAILURE",
            content={"relevant_tables": response_content},
            conversation_id=message.conversation_id
        )

# Simple test block
if __name__ == "__main__":
    agent = LibrarianAgent()
    test_msg = AgentMessage(
        sender="User", 
        receiver="Librarian", 
        performative="REQUEST", 
        content={"query": "Who are my top customers?"},
        conversation_id="test-123"
    )
    print(agent.process_request(test_msg))