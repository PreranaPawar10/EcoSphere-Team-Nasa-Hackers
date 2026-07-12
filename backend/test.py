# from sqlalchemy.exc import IntegrityError

# from app.crud import department_crud
# from app.database.db import SessionLocal
# from app.schemas import DepartmentCreate


# def main() -> None:
#     db = SessionLocal()

#     try:
#         department_data = DepartmentCreate(
#             name="Information Technology",
#             code="IT",
#             head="Gayatri Apte",
#             employee_count=20,
#             status=True,
#         )

#         department = department_crud.create(
#             db,
#             obj_in=department_data,
#         )

#         print("Department created successfully")
#         print("ID:", department.id)
#         print("Name:", department.name)
#         print("Code:", department.code)

#     except IntegrityError:
#         db.rollback()
#         print("A department with this name or code already exists.")

#     except Exception as error:
#         db.rollback()
#         print("Error:", type(error).__name__)
#         print(error)

#     finally:
#         db.close()


# if __name__ == "__main__":
#     main()

#GET opertaion
# from app.database.db import SessionLocal
# from app.crud import department_crud

# db = SessionLocal()

# department = department_crud.get(db, 1)

# if department:
#     print("Department Found")
#     print("ID:", department.id)
#     print("Name:", department.name)
#     print("Code:", department.code)
# else:
#     print("Department not found")

# db.close()

#DELETE
# from app.database.db import SessionLocal
# from app.crud import department_crud

# db = SessionLocal()

# deleted = department_crud.delete(
#     db,
#     record_id=1,
# )

# if deleted:
#     print("Deleted:", deleted.name)
# else:
#     print("Department not found")

# db.close()

#UPDATE
from app.database.db import SessionLocal
from app.crud import department_crud
from app.schemas import DepartmentUpdate

db = SessionLocal()

department = department_crud.get(db, 1)

updated_department = department_crud.update(
    db,
    db_object=department,
    obj_in=DepartmentUpdate(
        head="Gayatri Apte",
        employee_count=25,
    ),
)

print(updated_department.head)
print(updated_department.employee_count)

db.close()