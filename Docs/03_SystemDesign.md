# System Design – Electronic E-Commerce

## 1. Architecture Overview
The system follows a three-tier architecture:
1. **Presentation Layer:** HTML, CSS, JavaScript, Bootstrap/Tailwind (User Interface).
2. **Application Layer:** Django framework (Business Logic).
3. **Data Layer:** MySQL database (Data Storage).

## 2. User Roles & Access
| Feature                  | Customer | Shop Owner | Web App Admin |
|--------------------------|----------|------------|---------------|
| View Products            | ✅       | ✅         | ✅            |
| Add/Edit Products        | ❌       | ✅         | ✅            |
| Manage Orders (Own)      | ✅       | ✅         | ✅            |
| Manage All Orders        | ❌       | ❌         | ✅            |
| Manage Users             | ❌       | ❌         | ✅            |

## 3. Database ER Diagram (Conceptual)
**Entities:**
- User
- Shop
- Category
- Product
- ProductImage
- Cart
- CartItem
- Order
- OrderItem

(ERD diagram image to be added here – saved as `/docs/images/ERD.png`)

## 4. Technology Stack
- **Frontend:** HTML, CSS, JavaScript, Bootstrap/Tailwind
- **Backend:** Django
- **Database:** MySQL
- **Media Storage:** Local media folder (development), Cloud storage (production)
