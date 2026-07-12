# EcoSphere: ESG Management Platform - Team Nasa Hackers

# Our Team
Neevan Redkar - github.com/Neevs1 <br>
Pranav Ijantkar - github.com/Pranav-Ijantkar <br>
Prerana Pawar - github.com/PreranaPawar10 <br>
Gayatri Apte - github.com/gayatri-apte <br>

# Our approach
Components like authentication were designed first. Frontend and backend was developed parallely by teams of two. Proper planning was carried out to implement features in sprints, similar to agile methodology. Database was designed according to master mentioned in problem statement, and normalized further. APIs are document using swagger docs.
Frontend to Database data flow
Frontend JSON <br>
      ↓ <br>
Pydantic schema <br>
      ↓ <br>
   Router <br>
      ↓ <br>
Service / CRUD <br>
      ↓ <br>
SQLAlchemy model <br>
      ↓ <br>
PostgreSQL <br>

# Tech stack
Frontend - React (Vite) + TypeScript + Tailwind + shadcn/ui <br>
Backend - Python -> FastAPI, SQLAlchemy, Alembic <br>
Database - PostgreSQL