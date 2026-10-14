
from database import engine, Base
from models import TicketRecord

Base.metadata.create_all(bind=engine)

print("Database and ticket table created successfully!")
