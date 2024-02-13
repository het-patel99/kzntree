# myapp/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from kzntree.settings import CACHE_TIMEOUT
from .forms import RegistrationForm, LoginForm, CategoryForm, ItemForm, BuildDashboardForm
from django.contrib.auth.decorators import login_required
from .models import InventoryItem, Category, BuildDashboard
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import InventoryItemSerializer, BuildDashboardSerializer
from django.views.decorators.cache import cache_page

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')  # Redirect to your home page
        else:
            # Handle invalid login
            return render(request, 'registrations/login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'registrations/login.html')

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page after registration
    else:
        form = RegistrationForm()

    return render(request, 'registrations/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@api_view(['GET'])
def home_api(request):
    items = InventoryItem.objects.all()
    serializer = InventoryItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def build_dashboard_api(request):
    builds = BuildDashboard.objects.all()
    serializer = BuildDashboardSerializer(builds, many=True)
    return Response(serializer.data)

@cache_page(CACHE_TIMEOUT)
@login_required(login_url='login')  # Ensure users are logged in to access the home page
def home(request):
    items = InventoryItem.objects.all()  # Fetch all inventory items from the database
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'name_asc')

    # Filtering based on tags and category
    filter_by = request.GET.get('filter_by', '')

    if filter_by:
        if filter_by == 'tags':
            items = items.filter(tags__isnull=False)
        elif filter_by == 'category':
            items = items.filter(category__isnull=False)

    if sort_by == 'sku_asc':
        items = items.order_by('sku')
    elif sort_by == 'sku_desc':
        items = items.order_by('-sku')
    elif sort_by == 'name_asc':
        items = items.order_by('name')
    elif sort_by == 'name_desc':
        items = items.order_by('-name')
    elif sort_by == 'in_stock_asc':
        items = items.order_by('in_stock')
    elif sort_by == 'in_stock_desc':
        items = items.order_by('-in_stock')
    elif sort_by == 'available_stock_asc':
        items = items.order_by('available_stock')
    elif sort_by == 'available_stock_desc':
        items = items.order_by('-available_stock')

    if query:
        items = items.filter(
            Q(sku__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__icontains=query)
        )

    total_categories = Category.objects.count()
    total_items = items.count()

    context = {
        'items': items,
        'total_categories': total_categories,
        'total_items': total_items,
    }

    return render(request, 'home.html', context)


@login_required(login_url='login')
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@login_required(login_url='login')
def item_detail(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    return render(request, 'item_detail.html', {'item': item})

def build_detail(request, build_id):
    build = get_object_or_404(BuildDashboard, pk=build_id)
    # Other context data as needed

    return render(request, 'build_detail.html', {'build': build})

@cache_page(CACHE_TIMEOUT)
@login_required(login_url='login')
def build_dashboard(request):
    builds = BuildDashboard.objects.all()
    query = request.GET.get('q')
    # Filter builds
    if query:
        builds = builds.filter(
            Q(references__icontains=query) |
            Q(item_group__icontains=query) |
            Q(linked_sale_order_group__icontains=query)
        )
    filter_by = request.GET.get('filter_by')
    if filter_by:
        if filter_by == 'linked_sale_order_group':
            builds = builds.filter(linked_sale_order_group=request.GET.get('linked_sale_order_group'))
        elif filter_by == 'creation_group_date':
            builds = builds.filter(creation_group_date=request.GET.get('creation_group_date'))
        elif filter_by == 'completion_group_date':
            builds = builds.filter(completion_group_date=request.GET.get('completion_group_date'))

    # Sort builds
    sort_by = request.GET.get('sort_by')
    if sort_by:
        if sort_by == 'references':
            builds = builds.order_by('references')
        elif sort_by == 'quantity':
            builds = builds.order_by('quantity')
        elif sort_by == 'cost':
            builds = builds.order_by('cost')

    # Other data for the build dashboard
    pending_builds = builds.filter(completion_group_date__isnull=True).count()
    completed_builds = builds.exclude(completion_group_date__isnull=True).count()
    cancelled_builds = 0 
    most_built = 0  
    least_built = 0 

    context = {
        'builds': builds,
        'pending_builds': pending_builds,
        'completed_builds': completed_builds,
        'cancelled_builds': cancelled_builds,
        'most_built': most_built,
        'least_built': least_built,
    }

    return render(request, 'build.html', context)

@login_required(login_url='login')
def add_build(request):
    if request.method == 'POST':
        form = BuildDashboardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('build_dashboard')
    else:
        form = BuildDashboardForm()

    context = {
        'form': form,
    }

    return render(request, 'add_build.html', context)