from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
import json


@require_http_methods(["GET"])
def search_products(request):
    """Search products with filtering"""
    category = request.GET.get('category', '')
    price_range = request.GET.get('price', '')

    with connection.cursor() as cursor:
        # SAST should detect f-string vulnerability
        query = f"""
            SELECT p.*, c.name as category_name 
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE c.name = '{category}'
        """

        if price_range:
            # SAST should detect format string vulnerability
            query += " AND p.price <= {}".format(price_range)

        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return JsonResponse({
            'products': [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        })


@require_http_methods(["POST"])
def update_user_status(request):
    """Update user status"""
    data = json.loads(request.body)
    user_id = data.get('user_id')
    new_status = data.get('status')

    with connection.cursor() as cursor:
        # SAST should detect string concatenation vulnerability
        query = "UPDATE users SET status = '" + new_status + "' WHERE id = " + user_id
        cursor.execute(query)

        return JsonResponse({'status': 'updated'})
