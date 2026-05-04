from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime
import uuid

class AgentMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    
    sender: str  # e.g., "LibrarianAgent"
    receiver: str # e.g., "Orchestrator"
    
    # ACP Performatives
    # REQUEST: Ask for something
    # INFORM: Provide data
    # FAILURE: Report an error
    performative: str 
    
    content: Dict[str, Any] # The actual payload (e.g., {"relevant_tables": "orders"})
    conversation_id: str    # To track a specific conversation