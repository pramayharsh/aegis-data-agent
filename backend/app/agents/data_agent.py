import sqlite3
from ..protocols.acp import AgentMessage

class DataAgent:
    def __init__(self, db_path='aegis_mock.db'):
        self.db_path = db_path

    def execute_query(self, message: AgentMessage) -> AgentMessage:
        sql = message.content.get("sql")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql)
            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            conn.close()
            
            data = [dict(zip(columns, row)) for row in results]
            
            return AgentMessage(
                sender="DataAgent",
                receiver="User",
                performative="INFORM",
                content={"data": data, "row_count": len(data)},
                conversation_id=message.conversation_id
            )
        except Exception as e:
            return AgentMessage(
                sender="DataAgent",
                receiver="User",
                performative="FAILURE",
                content={"error": str(e)},
                conversation_id=message.conversation_id
            )