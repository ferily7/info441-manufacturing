# info441-manufacturing

## Brands

Creates a new brand in a form

POST:
```
{
  'name':'brand_name',
  'description':'description'
}
```
Response -> HTTP_200

## Carts

POST:
Add the specified product to the cart
```
{
  'name':'product_name',
  'description':'description',
  'quantity':'1',
  'price':'200',
  'product_type':[1],
  'seller':1
}
```
DELETE:
Deletes the specified 
Remove the specified product to the cart
```
{
  'name':'product_name',
  'description':'description',
  'quantity':'1',
  'price':'200',
  'product_type':[1],
  'seller':1
}
```

## Spec docs
Edit specifications
PATCH:
```
{
  'name':'spec_name',
  'description':'description',
  'creator':'1',
  'creator_type':'MN',
  'product':1,
  'content': ""
}
```
## Users
Create new user account

POST:
```
{
  'username':'user',
  'password':'pass',
  'passwordconf':'pass',
  'email':'test@email.com',
  'account_type':'BU',
  'street_adresss':'123 NE 4th ST.',
  'city':'Seattle',
  'state':'WA',
  'zipcode':98105
}
```
## Profiles
Edit user profile

PATCH:
```
{
  'user':'user',
  'account_type':'BU',
  'street_adresss':'123 NE 4th ST.',
  'city':'Seattle',
  'state':'WA',
  'zipcode':98105
}
```

## Purchases
Update purchase price and items

PATCH:
```
{
  'total_price':100
  'total_items':10
}
```
## Product Types
Create a new product type

POST:
```
{
  'name':'product_type',
  'description':'product_type_description',
}
```
## Products
Edit product name, description, quantity, and price 

PATCH:
```
{
  'name':'name',
  'description':'description',
  'quantity':1,
  'price':30
}
```
## Reviews
Edit review score and description

PATCH:
```
{
  'rating':5,
  'description':'description'
}
```
