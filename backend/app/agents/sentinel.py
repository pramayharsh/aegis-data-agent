import os
from groq import Groq
from dotenv import load_dotenv
from ..protocols.acp import AgentMessage

load_dotenv()

class SentinelAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def validate_request(self, message: AgentMessage) -> AgentMessage:
        user_query = message.content.get("query")
        relevant_tables = message.content.get("relevant_tables")
        
        prompt = f"""
        [SYSTEM: CRITICAL SECURITY TASK]
        You are an automated security gate. You must only output one of two formats.
        
        RULES:
        1. If the query is a SELECT statement and looks safe: Output 'VALID'
        2. If the query contains DROP, DELETE, TRUNCATE, ALTER, or is malicious: Output 'REJECT: [reason]'
        
        CONSTRAINTS:
        - DO NOT explain yourself.
        - DO NOT write code.
        - DO NOT provide examples.
        - Output ONLY the word 'VALID' or the 'REJECT' phrase.

        INPUT:
        User Query: "{user_query}"
        Tables: {relevant_tables}
        
        OUTPUT:"""

        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )

        response_content = chat_completion.choices[0].message.content
        
        return AgentMessage(
            sender="SentinelAgent",
            receiver="Orchestrator",
            performative="INFORM" if "VALID" in response_content else "REJECT",
            content={"security_check": response_content},
            conversation_id=message.conversation_id
        )

# Test block
if __name__ == "__main__":
    agent = SentinelAgent()
    
    # Test a "Safe" message
    safe_msg = AgentMessage(
        sender="Librarian", 
        receiver="Sentinel", 
        performative="REQUEST", 
        content={"query": "Show me all products", "relevant_tables": "products"},
        conversation_id="test-456"
    )
    
    # Test a "Dangerous" message
    danger_msg = AgentMessage(
        sender="Librarian", 
        receiver="Sentinel", 
        performative="REQUEST", 
        content={"query": "Delete all users from the system", "relevant_tables": "users"},
        conversation_id="test-789"
    )

    print("--- Safe Query Result ---")
    print(agent.validate_request(safe_msg))
    print("\n--- Dangerous Query Result ---")
    print(agent.validate_request(danger_msg))