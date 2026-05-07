from .agents.librarian import LibrarianAgent
from .agents.sentinel import SentinelAgent
from .agents.coder import CoderAgent
from .agents.data_agent import DataAgent
from .protocols.acp import AgentMessage
import uuid

class AegisMessageBus:
    def __init__(self):
        # Registering our agents in the system
        self.agents = {
            "LibrarianAgent": LibrarianAgent(),
            "SentinelAgent": SentinelAgent(),
            "CoderAgent": CoderAgent(),
            "DataAgent": DataAgent()
        }
        self.history = []

    def dispatch(self, message: AgentMessage):
        """The Post Office: Routes messages based on the 'receiver' field."""
        self.history.append(message)
        
        target_name = message.receiver
        
        # If the message is for the User/System, we stop and return the result
        if target_name == "User":
            return message

        if target_name in self.agents:
            print(f"[Bus] Delivering message from {message.sender} to {target_name}...")
            
            # This is the A2A call: The agent processes and decides who is next
            agent = self.agents[target_name]
            
            # Logic to route to the correct method based on agent type
            if target_name == "LibrarianAgent":
                response = agent.process_request(message)
                # Librarian logic: If success -> Next is Sentinel
                if response.performative == "INFORM":
                    response.receiver = "SentinelAgent"
                else:
                    response.receiver = "User"
            
            elif target_name == "SentinelAgent":
                response = agent.validate_request(message)
                # Sentinel logic: If valid -> Next is Coder
                if response.performative == "INFORM":
                    response.receiver = "CoderAgent"
                else:
                    response.receiver = "User"
            
            elif target_name == "CoderAgent":
                response = agent.generate_sql(message)
                response.receiver = "DataAgent"

            elif target_name == "DataAgent":
                response = agent.execute_query(message)
                # After getting data, send it back to the user
                response.receiver = "User"

            # Recursive call: Send the new message back to the bus
            return self.dispatch(response)
        
        else:
            return f"Error: Agent {target_name} not found."

# Full A2A System Test
if __name__ == "__main__":
    bus = AegisMessageBus()
    
    conv_id = str(uuid.uuid4())
    
    # User initiates the first message addressed to the Librarian
    entry_msg = AgentMessage(
        sender="User",
        receiver="LibrarianAgent", # Directed to Librarian
        performative="REQUEST",
        content={"query": "Which products cost more than 100?"},
        conversation_id=conv_id
    )

    print("--- Starting A2A Flow ---")
    final_response = bus.dispatch(entry_msg)
    print("\n--- Final System Output to User ---")
    print(final_response.content)