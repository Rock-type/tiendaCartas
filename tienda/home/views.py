from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Usuario, ProductoCartaYugioh, ProductoCartaMagic, Venta, VentaDetalle
from django.http import JsonResponse

MODELOS_CARTAS = {
    'Yu-Gi-Oh!': ProductoCartaYugioh,
    'Magic: The Gathering': ProductoCartaMagic,
}


def prueba(request):
    context = {
        'message': 'mensaje de prueb',
        'tareas': [
            'Trabajar',
            'Bailar',
            'Beber'
        ],
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'home/index.html',context)

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username  
    return render(request, 'home/home.html', context)

def registrar(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        usuario = Usuario(username=username, email=email)
        usuario.set_password(password)
        usuario.save()

        return redirect(reverse('registrar'))
    return render(request,'home/registrar.html')


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print('entro')
            return redirect(reverse('home'))  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'home/login.html')

def prueba2(request):
    caja_filtro = request.GET.get('caja', 'Darkwing Blast')
    orden = request.GET.get('orden', '1')  # Por defecto, '1' para alfabético

    if orden == '1':
        cartas = ProductoCartaYugioh.objects.filter(caja__nombre=caja_filtro).order_by('carta__nombre')
    elif orden == '2':
        cartas = ProductoCartaYugioh.objects.filter(caja__nombre=caja_filtro).order_by('-precio')
    elif orden == '3':
        cartas = ProductoCartaYugioh.objects.filter(caja__nombre=caja_filtro).order_by('precio')
    else:
        cartas = ProductoCartaYugioh.objects.filter(caja__nombre=caja_filtro)

    return render(request, 'home/vistaYugioh.html', {'cartas': cartas, 'orden': orden})




def busqueda(request):
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '1')
    cajas_seleccionadas = request.GET.getlist('cajas')
    rarezas_seleccionadas = request.GET.getlist('rarezas')
    tcg_seleccionados = request.GET.getlist('tcg')

    cartas = []
    tcg_frecuencia = {}
    cajas_frecuencia = {}
    rareza_frecuencia = {}

    # Consulta dinámica usando el diccionario de modelos
    for tcg, modelo in MODELOS_CARTAS.items():
        if not tcg_seleccionados or tcg in tcg_seleccionados:
            productos = modelo.objects.filter(carta__nombre__icontains=buscar)
            cartas.extend(productos)

            # Actualiza la frecuencia de los TCG
            if tcg in tcg_frecuencia:
                tcg_frecuencia[tcg] += len(productos)
            else:
                tcg_frecuencia[tcg] = len(productos)

    # Calcular la frecuencia de cartas por caja
    for carta in cartas:
        caja_nombre = carta.caja.nombre
        if caja_nombre in cajas_frecuencia:
            cajas_frecuencia[caja_nombre] += 1
        else:
            cajas_frecuencia[caja_nombre] = 1

    # Filtra por cajas seleccionadas
    if cajas_seleccionadas:
        cartas = [carta for carta in cartas if carta.caja.nombre in cajas_seleccionadas]

    # Ordena los resultados
    if orden == '1':
        cartas.sort(key=lambda x: x.carta.nombre)
    elif orden == '2':
        cartas.sort(key=lambda x: x.precio, reverse=True)
    elif orden == '3':
        cartas.sort(key=lambda x: x.precio)

    # Calcular la frecuencia de rarezas
    for carta in cartas:
        rareza = carta.rareza
        if rareza in rareza_frecuencia:
            rareza_frecuencia[rareza] += 1
        else:
            rareza_frecuencia[rareza] = 1

    # Filtra por rarezas seleccionadas
    if rarezas_seleccionadas:
        cartas = [carta for carta in cartas if carta.rareza in rarezas_seleccionadas]

    # Marca cartas sin stock
    for carta in cartas:
        carta.has_stock = carta.stock < 1

    for carta in cartas:
        cantidad = list(range(1, carta.stock + 1))
        carta.cantidad_lista=cantidad

    return render(request, 'home/vistaYugioh.html', {
        'cartas': cartas,
        'orden': orden,
        'buscar': buscar,
        'totalBusqueda': len(cartas),
        'cajas_frecuencia': cajas_frecuencia,
        'rarezas': rareza_frecuencia,
        'cajas_seleccionadas': cajas_seleccionadas,
        'rarezas_seleccionadas': rarezas_seleccionadas,
        'tcg_frecuencia': tcg_frecuencia,
        'tcg_seleccionados': tcg_seleccionados
    })


def carroVista(request):
    carrito = request.session.get('carrito', {})
    productos = []
    cantidadProductos = 0
    monto = 0

    for item_key, item_data in carrito.items():
        modelo = MODELOS_CARTAS[item_data['tcg']]
        
        carta = modelo.objects.get(
            carta__id=item_data['carta_id'],
            caja__id=item_data['caja_id'],
            rareza=item_data['rareza']
        )

        cantidad_lista = list(range(1, carta.stock + 1))

        totalProducto = carta.precio * item_data['cantidad']
        monto += totalProducto
        cantidadProductos += item_data['cantidad']
        
        productos.append({
            'carta': carta,
            'cantidad': item_data['cantidad'],
            'total': "{:.2f}".format(item_data['total']),
            'idCarro':item_key,
            'cantidad_lista': cantidad_lista
        })

    context = {
        'productos': productos,
        'cantidadProductos': cantidadProductos,
        'monto': monto
    }

    #print('Productos ',productos)

    return render(request, 'home/carro_compra.html', context)


def agregar_carro(request):
    carta_id = request.GET.get('carta', '')
    cantidad_carta = int(request.GET.get('cantidad', '1'))
    caja_id = request.GET.get('caja', '')
    rareza = request.GET.get('rareza', '')
    tcg = request.GET.get('tcg','')


    carrito = request.session.get('carrito', {})

    modelo = MODELOS_CARTAS.get(tcg, None)
    carta = modelo.objects.get(carta__id=carta_id, caja__id=caja_id, rareza=rareza)

    item_key = f"{carta_id}-{caja_id}-{rareza}"
    
    if item_key in carrito:
        if carta.stock < carrito[item_key]['cantidad'] + cantidad_carta:
            mensaje = "El carrito excede el stock"
            return JsonResponse({'status': 'error', 'message': mensaje})
        carrito[item_key]['cantidad'] += cantidad_carta
    else:
        carrito[item_key] = {
            'cantidad': cantidad_carta,
            'caja_id': caja_id,
            'rareza': rareza,
            'tcg': tcg,
            'carta_id':carta_id,
            'precio_unitario': float(carta.precio),
            'total': float(cantidad_carta * carta.precio) 
        }
    print(carrito[item_key])
    request.session['carrito'] = carrito

    mensaje = 'Productos agregados al carrito.' if cantidad_carta > 1 else 'Producto agregado al carrito.'
    
    return JsonResponse({'status': 'success', 'message': mensaje})


def eliminarProductoCarro(request, id):
    carrito = request.session.get('carrito', {})
    if id in carrito:
        del carrito[id]  
    request.session['carrito'] = carrito
    return redirect('carroVista')

def eliminarCarro(request):
    request.session['carrito'] = {}  # Restablecer el carrito a un diccionario vacío
    return redirect('carroVista')


def modificarCantidadCarro(request, id, cantidad):
    carrito = request.session.get('carrito', {})
    if id in carrito:
        carrito[id]['cantidad'] = cantidad
        carrito[id]['total'] = cantidad * carrito[id]['precio_unitario']
        request.session['carrito'] = carrito
        return JsonResponse({'status': 'success', 'redirect': '/carro/'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Producto no encontrado en el carrito.'})


def realizarCompra(request):
    carrito = request.session.get('carrito', {})
    errores = []

    for llave, data in carrito.items():
        modelo = MODELOS_CARTAS[data['tcg']]
        carta = modelo.objects.get(carta__id=data['carta_id'], caja__id=data['caja_id'], rareza=data['rareza'])

        if data['cantidad'] > carta.stock:
            errores.append(carta.carta.nombre)
            data['cantidad'] = carta.stock
            data['total'] = float(carta.stock * carta.precio)
        else:
            print(carta.carta.nombre, " Todo bien ", carta.stock - data['cantidad'])

 
    request.session['carrito'] = carrito


    if errores:
        error_message = (
            "Los siguientes productos exceden el stock actual. La cantidad ha sido ajustada al stock disponible:<br>"
            "<ul>" + "".join([f"<li>{error}</li>" for error in errores]) + "</ul>"
        )
        messages.error(request, error_message)
    else:
        try:

            # Crear la venta
            venta = Venta.objects.create(
                usuario=request.user,
                total=sum(item['total'] for item in carrito.values()),
                estado='PROCESANDO'
            )

            for llave, data in carrito.items():
                modelo = MODELOS_CARTAS[data['tcg']]
                carta = modelo.objects.get(carta__id=data['carta_id'], caja__id=data['caja_id'], rareza=data['rareza'])
                producto_venta = VentaDetalle.objects.create(
                    venta=venta,
                    producto=data['carta_id'],  # Pasar el objeto 'Carta' en lugar del nombre
                    cantidad=data['cantidad'],
                    precio_unitario=data['precio_unitario'],
                    precio_total=data['total'],
                    juego=data['tcg']
                )
                carta.stock -= data['cantidad']
                carta.save()
                
            
            request.session['carrito'] = {}

            messages.success(request, "Compra realizada exitosamente.")

        except Exception as e:
            # Manejo de errores en la transacción
            messages.error(request, f"Hubo un problema al procesar tu compra: {str(e)}")

    return redirect('carroVista')