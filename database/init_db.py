from db import engine, Base
import models

# 4. Physically trigger file and table initialization
Base.metadata.create_all(bind=engine)

print("database initialized successfully")