from fastapi import FastAPI


from graphene import ObjectType, List, String, Schema, Field, Int, Mutation


from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp
from schemas import Account, CourseType, Emails, UserIdentifier


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


"""
query{
  getData(id: 6) {
    id
    name
    email
    password
  }
}
"""

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


"""
mutation structure that returns all the data if the 
insertion is successful
mutation {
  createUser(
    email:"r@gmailcom"
    name:"ravi"
    password:"password"
  ) {
    newUser {
      id
      name
      email
      password
    }
  }
}
"""
class CreateUser(Mutation):
	new_user = Field(Account)

	class Arguments:
		#id: String(required=True)
		name= String(required=True)
		email=String(required=True)
		password = String(required=True)

	async def mutate(self, info, name, email, password):
		detail = crud.create_user(name, email, password)
		return CreateUser(detail)

class UserMutation(ObjectType):
	create_user = CreateUser.Field()





"""
mutation structure that returns email if the 
insertion is successful
mutation {
  createUser(
    email:"r@gmailcom"
    name:"ravi"
    password:"password"
  ) {
    newUser {
      id
      name
      email
      password
    }
  }
}
"""
class CreateAccount(Mutation):
	new_user_id = Field(Emails)
	class Arguments:
		name= String(required=True)
		email=String(required=True)
		password = String(required=True)

	async def mutate(self, info, name, email, password):
		detail = crud.create_user(name, email, password)
		return CreateAccount(detail)

class NewAccMutation(ObjectType):
	create_account = CreateAccount.Field()

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

#returns entire inserted data when insertion is successful
app.add_route("/new_user", GraphQLApp(
  schema=Schema(query=UsersQuery, mutation=UserMutation),
  executor_class=AsyncioExecutor)
)


#returns email id when insertion is successful
app.add_route("/new_account", GraphQLApp(
  schema=Schema(query=EmailQuery, mutation=NewAccMutation),
  executor_class=AsyncioExecutor)
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)