from graphene import String, ObjectType, Boolean

from typing import List, Optional#, EmailStr

from pydantic import BaseModel

class Account(ObjectType):
	id = String(required=True)
	name = String(required=True)
	password = String(required=True)
	email = String()


class UserIdentifier(ObjectType):
	id = String(required=True)


class Emails(ObjectType):
	# id = String(required=True)
	# name = String(required=True)
	# password = String(required=True)
	email = String()

class UploadResponse(ObjectType):
	result = Boolean()

class CourseType(ObjectType):
  id = String(required=True)
  title = String(required=True)
  instructor = String(required=True)
  publish_date = String()



class NewUser(BaseModel):
	name: str
	email: str
	password: str
