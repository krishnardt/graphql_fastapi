from fastapi import FastAPI


from graphene import ObjectType, List, String, Schema, Field, Int


from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp
from schemas import Account, CourseType, Emails


#from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
import uvicorn
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

####################Query and mutation resolvers################
class UsersQuery(ObjectType):
	"""
	to get all the user details in the database.
	result:
	returns dict of users
	"""
	user_list = None
	get_users = List(Account)
	async def resolve_get_users(self, info):
		app_users = crud.get_users()
		return app_users


class EmailQuery(ObjectType):
	"""
	to get all the email of all users in the database.
	result:
	returns dict of emails
	"""
	user_list = None
	get_emails = List(Emails)
	async def resolve_get_emails(self, info):
		app_users = crud.get_users()
		print(app_users)
		return app_users



class UserId(ObjectType):
	"""
	input:
	id: the user_id
	result:
	returns the details of the given user_id
	"""
	user_detail = None
	get_data = Field(Account,id=Int())
	async def resolve_get_data(self, info, id):
		app_users = crud.get_users()
		for user in app_users:
			print(user)
			if user['id'] == id:
				return user
		return None


#####################Rotues###########################
app.add_route("/", GraphQLApp(
  schema=Schema(query=UsersQuery),
  executor_class=AsyncioExecutor)
)


app.add_route("/emails", GraphQLApp(
  schema=Schema(query=EmailQuery),
  executor_class=AsyncioExecutor)
)

app.add_route("/user", GraphQLApp(
  schema=Schema(query=UserId),
  executor_class=AsyncioExecutor)
)


# @app.post("/new_user")#, response_model=schemas.Users)
# async def create_user(user: schemas.NewUser, db: Session = Depends(get_db)):
#     temp = user.__dict__
#     print(temp)
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     insert_status = crud.create_user(db=db, user=user)
#     print(insert_status)
#     return insert_status



# @app.get("/users")#, response_model=List[schemas.Users])
# async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)