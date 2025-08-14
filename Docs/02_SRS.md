# Software Requirements Specification – Electronic E-Commerce

## 1. Functional Requirements

### 1.1 User Management
- Registration and login for all roles.
- Role-based access control (Customer, Shop Owner Admin, Web App Admin).
- Profile management with profile picture upload.

### 1.2 Product Management
- Shop owners can add, edit, and delete products.
- Products have categories, prices, stock quantity, and main image.
- Additional product images allowed.

### 1.3 Shop Management
- Shop creation linked to shop owner.
- Shop logo and description stored.
- Shop owners can only manage their own shops.

### 1.4 Order Management
- Customers can add items to cart and checkout.
- Order creation stores products, quantity, and price at purchase.
- Order status tracking: Pending → Processing → Shipped → Delivered.
- Shop owners see orders related to their products only.
- Web admins see all orders.

### 1.5 Media Handling
- Product images stored securely.
- Shop logos stored separately.
- User profile pictures stored in a designated folder.

---

## 2. Non-Functional Requirements
- **Security:** Passwords hashed, role-based restrictions.
- **Performance:** Load product listings efficiently.
- **Usability:** Mobile-friendly UI.
- **Scalability:** Able to support more shops and products in the future.

---

## 3. Data Requirements
### Entities:
- User (with role)
- Shop
- Category
- Product
- ProductImage
- Cart
- CartItem
- Order
- OrderItem

---

## 4. External Interfaces
- Payment gateway integration (future enhancement).
- Map API for delivery tracking (future enhancement).
