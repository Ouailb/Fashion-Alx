# Api


## -------------------------------- Users --------------------------------
### [GET]:
* api/users  (get all users)
* api/users/<int:user_id>  (get a specific user)

### [POST]:
* api/users (post new user) (params: email, password, first_name, last_name, address, phone)

### [PUT]:
* api/users/<int:user_id>  (update user)

### [DELETE]:
* api/users/<int:user_id>  (delete user)

## -------------------------------- Products --------------------------------
### [GET]:
* api/products (get all products)
* api/products/<int:product_id>  (get a specific product)

### [POST]:
* api/products  (post new product) (params: brand, price, description, category_id)

### [PUT]:
* api/products/<int:product_id>  (update product)

### [DELETE]:
* api/products/<int:product_id>   (delete product)

## -------------------------------- Orders/items --------------------------------
### [GET]:
* api/users/<int:user_id>/orders (get all user orders)
* api/users/<int:user_id>/orders/<int:order_id>  (get a specific order)
* api/users/<int:user_id>/orders/<int:order_id>/items (get all order items)
* api/users/<int:user_id>/orders/<int:order_id>/items/<int:item_id> (get a specific item)

### [POST]:
* api/users/<int:user_id>/orders/ (post new order) (params: No Param)
* api/users/<int:user_id>/orders/<int:order_id>/items (post order_item) (params: product_id)

### [PUT]:
* api/users/<int:user_id>/orders/<int:order_id> (update order)

### [DELETE]:
* api/users/<int:user_id>/orders/<int:order_id> (delete order)
* api/users/<int:user_id>/orders/<int:order_id>/items/<int:item_id> (delete item from order_items)

