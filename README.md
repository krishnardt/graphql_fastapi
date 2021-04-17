# graphql_fastapi

techstack in this repo:
1. FastAPI
2. PostgresQL
3. graphene
4. uvicorn(you can use gunicorn if your python is > 3.7)


small learning project to explore graphql

Things you will get in this repo:
1. get --> Query
2. post --> mutation
3. update --> mutation
4. delete --> mutation


routes:
1. getting data - Done
2. filtering data - Done
3. inserting_data - Done
4. deleting data
5. getting nested data
6. search using graphene
7. upload files



resources:
for graphql datatypes or scalars:
https://docs.graphene-python.org/en/latest/types/scalars/

reference link:
https://blog.logrocket.com/building-a-graphql-server-with-fastapi/


mutation explanation

lets have a look at the CreateAccount mutation code;
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
"""

when inserting a new user details, we need it to be extended with mutation.
new_user_id --> this is the reponse data when the insertion is successful
example repsonse would be look like:
{
  "data": {
    "createAccount": {
      "newUserId": {
        "email": "ra@gmailcom"
      }
    }
  }
}

Arguments is the input fields required to fill/create the new_user.

mutate is the function that contains the insertion logic.
mutate function connects to the backend crud function to insert the data
and the returned data(if it successful) will be wrapped with CreateAccount class.


This is just a definition how the new user mutation look like.

We need to define it with the Field datatype in order to use it.

