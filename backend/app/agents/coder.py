import os
from groq import Groq
from dotenv import load_dotenv
from ..protocols.acp import AgentMessage

load_dotenv()

class CoderAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # The Coder needs the schema details to write correct SQL
        self.catalog = """
        TABLE: customers (columns: id, name, email, join_date)
        TABLE: orders (columns: id, customer_id, order_date, total_amount)
        TABLE: products (columns: id, product_name, price)
        """

    def generate_sql(self, message: AgentMessage) -> AgentMessage:
        user_query = message.content.get("query")
        relevant_tables = message.content.get("relevant_tables")
        
        prompt = f"""
        You are an expert SQL Developer. Generate a Postgres SQL query based on the user's request.
        
        SCHEMA CONTEXT:
        {self.catalog}

        USER REQUEST: "{user_query}"
        TABLES TO USE: {relevant_tables}

        RULES:
        1. Use ONLY the tables provided above.
        2. Generate ONLY 'SELECT' queries.
        3. Do not use table aliases unless necessary.
        4. Output ONLY the raw SQL string. 
        5. No markdown formatting (no ```sql blocks).
        6. No explanations.
        """

        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )

        sql_code = chat_completion.choices[0].message.content
        
        return AgentMessage(
            sender="CoderAgent",
            receiver="Orchestrator",
            performative="PROPOSE", # In ACP, we use PROPOSE for a suggested solution
            content={"sql": sql_code},
            conversation_id=message.conversation_id
        )

# Test block
if __name__ == "__main__":
    agent = CoderAgent()
    
    test_msg = AgentMessage(
        sender="Orchestrator", 
        receiver="Coder", 
        performative="REQUEST", 
        content={
            "query": "Get the names of customers who spent more than 100 dollars", 
            "relevant_tables": "customers, orders"
        },
        conversation_id="test-cod-1"
    )

    print("--- Generated SQL ---")
    print(agent.generate_sql(test_msg))