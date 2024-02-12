# kzntree

[![GitHub license](https://img.shields.io/github/license/het-patel99/kzntree)](https://github.com/het-patel99/kzntree/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/het-patel99/kzntree)](https://github.com/het-patel99/kzntree/issues)
[![GitHub stars](https://img.shields.io/github/stars/het-patel99/kzntree)](https://github.com/het-patel99/kzntree/stargazers)

## Description

KZNTree is an inventory management Django application with RESTful API.

## Video Explanation

[![Your Video](https://img.youtube.com/vi/zlDP3ZM8mnA/1.jpg)](https://youtu.be/zlDP3ZM8mnA?si=8w437ir6BBs1kPZL)


## Setup and Run

Follow these steps to set up and run the application locally:

1. **Clone the Repository:**
    ```
    git clone https://github.com/het-patel99/KZNTree.git
    cd KZNTree
    ```
2. **Install all the requirements:**
    ```
    pip install -r requirements.txt
    ```
3. **Run Migrations**
    ```
    python manage.py migrate
    ```
4. **Start the server**
    ```
    python manage.py runserver
    kzntree server should start at  http://localhost:8000.
    GO to below link for login page or register page directly and then you can interact seamlessly.
    http://localhost:8000/accounts/login/
    http://localhost:8000/acocunts/register/
    ```

## API Descriptions

Auto-Documentation for REST APIs with DRF-Swagger in done in this Django application . 
    Test API
    http://localhost:8000/swagger/


1. Home API

    Endpoint: /accounts/api/home/
    Location: http://localhost:8000/api/home/

    Description: Fetches data related to inventory items.

    Request URL: http://localhost:8000/accounts/api/home/
    Response Response body
    ```
        [
            {
                "id": 1,
                "sku": "ETSY-FOREST",
                "name": "Etsy Bundle Pack",
                "tags": "ESDC",
                "in_stock": 0,
                "available_stock": 0,
                "category": 1
            }
        ]
    ```


2. Build Dashboard API
    
    Endpoint: /accounts/api/build_dashboard/
    Location: http://localhost:8000/api/build_dashboard/

    Description: Fetches data related to the build dashboard.
    Request URL: http://localhost:8000/accounts/api/build_dashboard/
    Response Response body
    ```
        [
            {
                "id": 1,
                "references": "Build 3-Pack Single Beeswax Wrap for SO #1002",
                "item_group": "2-packSingle Beeswax Wrap",
                "quantity": 100,
                "cost": "525.00",
                "linked_sale_order_group": "SO #1002",
                "creation_group_date": "2023-02-24",
                "completion_group_date": null
            }
        ]
    ```


## Caching
Django provides a simple API for adding caching to views using decorators. Below, I'll show you how you can add caching to your home and build dashboard APIs. Caching is implemented to optimize the performance of the APIs. The cache timeout is set to CACHE_TIMEOUT seconds.
```
# settings.py

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

```
@cache_page(CACHE_TIMEOUT) 
@api_view(['GET'])
def home_api(request):
    ""details""

@cache_page(CACHE_TIMEOUT)  
@api_view(['GET'])
def build_dashboard_api(request):
    ""details""
```



## Thanks for reaching at the end of this project. Hope you enjoyed this Django Application.