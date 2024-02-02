# Ecommerce-API

## Overview

Ecommerce-API is a Django-based e-commerce RESTful API developed by Feliciano Candieiro. This API provides functionality for managing products, categories, user accounts, addresses, orders, comments, and tags.

## Installation

To set up the Ecommerce-API, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/felicianocandieiro/Ecommerce-API.git
   ```

2. Install dependencies using the following command:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Dependencies

The following Python packages were used in the development of this project:

- asgiref==3.2.10
- Django==3.0
- django-cors-headers==3.1.1
- django-polymorphic==3.1.0
- djangorestframework==3.10.3
- djangorestframework-jwt==1.11.0
- djangorestframework-simplejwt==5.2.2
- mysqlclient==2.1.1
- PyJWT==1.7.1
- pytz==2020.1
- sqlparse==0.3.1

## URLs

### Project URLs

The main project URLs are defined in the `urls.py` file:

```python
# Ecommerce-API URLs
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('products.urls', namespace='products')),
    path('api/', include('comments.urls', namespace='comments')),
    path('api/', include('addresses.urls', namespace='addresses')),
    path('api/', include('orders.urls', namespace='orders')),
    path('api/', include('users.urls', namespace='users')),
    path('api/', include('tags.urls', namespace='tags')),
    path('api/', include('categories.urls', namespace='categories')),
]
```

### User URLs

User-related URLs are defined in `users.urls`:

```python
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from users.views import Register

app_name = 'users'

urlpatterns = [
    url(r'^users', Register.as_view()),
    url(r'^users/register', Register.as_view()),
    url(r'^users/login', obtain_jwt_token),
    url(r'^auth/login', obtain_jwt_token),
]
```

### Address URLs

Address-related URLs are defined in `addresses.urls`:

```python
from django.conf.urls import url
from addresses.views import AddressListView

app_name = 'addresses'

urlpatterns = [
    url(r'^addresses$', AddressListView.as_view(), name='address_list'),
]
```

### Category URLs

Category-related URLs are defined in `categories.urls`:

```python
from django.conf.urls import url
from categories.views import CategoryListCreateView

app_name = 'categories'

urlpatterns = [
    url(r'^categories/?$', CategoryListCreateView.as_view(), name='category_create_list'),
]
```

### Comment URLs

Comment-related URLs are defined in `comments.urls`:

```python
from django.conf.urls import url
from comments.views import CommentListView, CommentDetailsView

app_name = 'comments'

urlpatterns = [
    url(r'^products/(?P<slug>([a-z0-9-])+)/comments$', CommentListView.as_view(), name='comment_list'),
    url(r'^comments/(?P<pk>([a-z0-9-])+)$', CommentDetailsView.as_view(), name='comment_details_short'),
    url(r'^products/(?P<slug>([a-z0-9-])+)/comments/(?P<pk>([a-z0-9-])+)$', CommentDetailsView.as_view(), name='comment_details'),
]
```

### Order URLs

Order-related URLs are defined in `orders.urls`:

```python
from django.conf.urls import url
from orders.views import OrderListView, OrderDetailsView

app_name = 'orders'

urlpatterns = [
    url(r'^orders/?$', OrderListView.as_view(), name='order_list'),
    url(r'^orders/(?P<pk>([a-z0-9-])+)$', OrderDetailsView.as_view(), name='order_details'),
]
```

### Product URLs

Product-related URLs are defined in `products.urls`:

```python
from django.urls import re_path as url
from products.views import ProductListView, ProductDetailsView

app_name = 'products'

urlpatterns = [
    url(r'^products$', ProductListView.as_view(), name='product_list'),
    url(r'^products/(?P<slug>([a-z0-9-])+)$', ProductDetailsView.as_view(), name='product_details'),
    url(r'^products/by_id/(?P<pk>([a-z0-9-])+)$', ProductDetailsView.as_view(), name='product_details_by_id'),
]
```

## Contributors

- Feliciano Candieiro (GitHub: [felicianocandieiro](https://github.com/catson28))

Feel free to contribute by opening issues or submitting pull requests!

## License

This project is licensed under the [MIT License](LICENSE).