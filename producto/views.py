from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import ProductoForm
from .models import Producto

# Create your views here.

# Home de la aplicación 
def home(request):
    return render(request, 'home.html')

# Formulario para crear user
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm,
        })
    else: 
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('productos')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exist'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
        })

# Funcion que permite cerrar la sesion del usuario
def signout(request):
    logout(request)
    return redirect('home')

# Esta funcion se encarga de listar los productos
def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

# Esta funcion se encarga de insertar un producto
def ingresar_producto(request):
    if request.method == 'GET':
        return render(request, 'ingresar_producto.html',{
            'form': ProductoForm
        })
    else: 
        try:
            form = ProductoForm(request.POST)
            ingresar_producto = form.save(commit=False)
            ingresar_producto.save()
            return redirect('productos')
        except ValueError:
            return render(request, 'ingresar_producto.html',{
                'form': ProductoForm
            })

# Inicio de sesión
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signin.html',{
                'error': 'Credenciales Erroneas'
            })
    else:
        return render(request, 'signin.html')
