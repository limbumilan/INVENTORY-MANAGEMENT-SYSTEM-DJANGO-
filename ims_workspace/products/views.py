from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Product
from .forms import StockMovementForm

def inventory_dashboard(request):
    # 1. If the user clicked "Submit" (POST request)
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            try:
                # Save the transaction log (This will automatically trigger our stock signal math!)
                form.save()
                messages.success(request, "Stock ledger updated successfully!")
                return redirect('inventory_dashboard')
            except ValidationError as e:
                # If our automated signal catches an error (like negative stock), display it
                messages.error(request, f"Transaction Failed: {e.message}")
    
    # 2. If the user is just looking at the page (GET request)
    else:
        form = StockMovementForm()

    # Fetch live database information to display in the table
    all_products = Product.objects.all()
    
    context = {
        'products': all_products,
        'form': form
    }
    return render(request, 'products/dashboard.html', context)

import csv
from django.http import HttpResponse

def export_inventory_csv(request):
    # 1. Create the browser response header pointing to a CSV download attachment
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="live_inventory_report.csv"'
    
    # 2. Open a CSV writer tool
    writer = csv.writer(response)
    
    # 3. Write the Excel Column headers
    writer.writerow(['Product Name', 'SKU', 'Category', 'Price', 'Current Stock'])
    
    # 4. Pull all matching records directly from your database
    products = Product.objects.all()
    for product in products:
        # Get the current quantity safely, defaulting to 0 if none exists
        stock_qty = product.inventory.quantity if hasattr(product, 'inventory') else 0
        
        writer.writerow([product.name, product.sku, product.category, product.price, stock_qty])
        
    return response