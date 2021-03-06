from fastapi import FastAPI
import ast

from graphene import ObjectType, List, String, Schema, Field, Int, Mutation, Boolean, ClientIDMutation
from graphene_file_upload.scalars import Upload


from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp
from schemas import Account, Emails, UserIdentifier, UploadResponse


#from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
import uvicorn
from shutil import copyfile
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


'''
mutation {
  uploadFile(
    filedata :"/home/spyder/Downloads/KrishnaMohanInjeti_3_years_SE_experience_resume_1.pdf"
  ) {
    success
  }
}
'''
class UploadFileSingle(Mutation):

	class Arguments:
	    filedata = Upload()

	filedata = List(Upload)
	success = Boolean()


	def mutate(self, info,  filedata=None):
		print(type(filedata))
		print(filedata.value)
		# with open(filedata.value, 'rb') as f:
		# 	print(f.read())

		#date_file = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		#date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		#dateplus = date + ".txt"
		#fs = FileSystemStorage()
		#fs.save(dateplus,filedata[0])
		#dest = "filename"#r'/home/spyder/KrishnaMohanInjeti_3_years_SE_experience_resume_1.pdf'
		#copyfile(r'{}'.format(filedata.value), dest)
		return UploadFileSingle(success=True)


'''
mutation {
  uploadFiles(
    filedata :[
      "/home/spyder/Downloads/KrishnaMohanInjeti_3_years_SE_experience_resume_1.pdf",
      "/home/spyder/Downloads/fastapi_3059.py"
    ]
      
  ) {
    success
  }
}
'''
class UploadFileMultiple(Mutation):

	class Arguments:
	    filedata = Upload()

	filedata = List(Upload)
	success = Boolean()


	def mutate(self, info,  filedata=None):
		print(type(filedata))
		print(filedata)
		files_list = filedata.values
		for files in files_list:
			print(files.value)
		# with open(filedata.value, 'rb') as f:
		# 	print(f.read())

		#date_file = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		#date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		#dateplus = date + ".txt"
		#fs = FileSystemStorage()
		#fs.save(dateplus,filedata[0])
		#dest = "filename"#r'/home/spyder/KrishnaMohanInjeti_3_years_SE_experience_resume_1.pdf'
		#copyfile(r'{}'.format(filedata.value), dest)
		return UploadFileMultiple(success=True)



class SingleFileUploadMutation(ObjectType):
	upload_file = UploadFileSingle.Field()


class MultipleFileUploadMutation(ObjectType):
	upload_files = UploadFileMultiple.Field()

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



class DeleteAccount(Mutation):
	success = Field(UploadResponse)
	class Arguments:
		name=String(required=True)

	async def mutate(self, info, name):
		detail = crud.delete_user(name)
		print(detail)
		return DeleteAccount(success=UploadResponse(result=detail))

class DeleteAccMutation(ObjectType):
	delete_account = DeleteAccount.Field()

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


#for single file upload
app.add_route("/upload", GraphQLApp(
  schema=Schema(query=UploadResponse ,mutation=SingleFileUploadMutation),
  executor_class=AsyncioExecutor)
)

#for multiple files upload
app.add_route("/uploads", GraphQLApp(
  schema=Schema(query=UploadResponse ,mutation=MultipleFileUploadMutation),
  executor_class=AsyncioExecutor)
)

app.add_route("/remove", GraphQLApp(
  schema=Schema(query=UploadResponse ,mutation=DeleteAccMutation),
  executor_class=AsyncioExecutor)
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
