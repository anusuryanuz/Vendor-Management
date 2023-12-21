# Vendor Management System

This is a Django-based Vendor Management System that handles vendor profiles, purchase orders, and calculates vendor performance metrics.

## Table of Contents
- Features
- Installation
- Usage
- API Endpoints
- Backend Logic for Performance Metrics
- Additional Technical Considerations
  

## Features

1. **Vendor Profile Management:**
    - Create, list, retrieve, update, and delete vendor profiles.
    
2. **Purchase Order Tracking:**
    - Create, list, retrieve, update, and delete purchase orders.
    - Filter purchase orders by vendor.

3. **Vendor Performance Evaluation:**
    - Calculate and retrieve performance metrics for vendors.
    - Metrics include on-time delivery rate, quality rating average, average response time, and fulfillment rate.

4. **Historical Performance Tracking:**
    - Optionally store historical data on vendor performance.
    - Enables trend analysis over time.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/anusuryanuz/Vendor-Management
    cd vendor_management
    ```

2. Install dependencies:

    ```bash
    pip install django
    pip install djangorestframework
    ```

3. Run migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. admin
   username: an
   password: 123
## Usage

1. Start the development server:

    ```bash
    python manage.py runserver
    ```

2. Access the API at  http://127.0.0.1:8000/
    http://127.0.0.1:8000/admin - for admin
    http://127.0.0.1:8000/api - for apis

## API Endpoints

- **Vendor Endpoints:**
    - '/api/vendors/`: Create a new vendor & List all vendors
    -  '/api/vendors/<int:pk>/`: Retrieve a specific vendor's details,update and delete vendor
       (in here int:pk is used instead of vendor_id to provide security for vendor datas )
- **Purchase Order Endpoints:**
    - `/api/purchase_orders/`: Create a new purchase order & List all purchase orders.
    - `/api/purchase_orders/<int:pk>/`: Retrieve,update and delete details of a specific purchase order.
- **Vendor Performance Endpoints:**
    - `GET /api/vendors/<int:pk>/performance`: Retrieve a vendor's performance metrics.
- **update a vendors order acknowledgement :**
    - '/api/purchase_orders/<int:pk>/acknowledge/`:

## over all urls
   admin/
api/ vendors/ [name='vendor-list-create']
api/ vendors/<int:pk>/ [name='vendor-detail']
api/ vendors/<int:pk>/performance/ [name='vendor-performance']
api/ purchase_orders/ [name='purchase-order-list-create']
api/ purchase_orders/<int:pk>/ [name='purchase-order-detail']
api/ purchase_orders/<int:pk>/acknowledge/ [name='purchase-order-acknowledge']
