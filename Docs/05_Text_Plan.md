# Test Plan – Electronic E-Commerce

## 1. Test Cases

| ID   | Feature              | Test Description                        | Expected Result                         | Status |
|------|----------------------|-----------------------------------------|-----------------------------------------|--------|
| TC01 | Registration         | Register as a new customer              | Account created, redirect to login      | Pass   |
| TC02 | Login                | Login with valid credentials            | Dashboard visible                       | Pass   |
| TC03 | Add Product          | Shop owner adds a new product           | Product appears in shop catalog         | Pass   |
| TC04 | Cart Add             | Customer adds item to cart              | Item visible in cart                    | Pass   |
| TC05 | Checkout             | Complete checkout process               | Order created, status = Pending         | Pass   |
| TC06 | Order Status Update  | Shop owner changes order status         | Customer sees updated status            | Pass   |
| TC07 | Role Restriction     | Customer tries to access admin page     | Access denied                           | Pass   |
