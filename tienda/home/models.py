from django.db import models
from django.contrib.auth.models import AbstractUser


class Administrador(models.Model):
    username = models.CharField(max_length=16, blank=False, null=False)
    password = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.username

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=10,blank=True, null=True)

    def __str__(self):
        return self.username

class Carta(models.Model):
    nombre = models.CharField(max_length=50,blank=False,null=False, verbose_name="Nombre de la carta")
    descripcion = models.TextField(verbose_name="Descripcion de la carta")

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre

class Caja(models.Model):
    nombre = models.CharField(max_length=50,blank=False, null=False, verbose_name="Nombre de la caja")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripcion de la caja")

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre
        


class CartaYugioh(Carta):
    juego = models.CharField(default='Yu-Gi-Oh!', max_length=50, verbose_name="Juego de cartas")

    def __str__(self):
        return self.nombre

class cajaYugioh(Caja):
    stock = models.IntegerField(blank=False, null=False, verbose_name="Cantidad en existencias")
    precio = models.DecimalField(blank=False, null=False, verbose_name="Precio del producto", decimal_places=2, max_digits=6)
    preventa = models.BooleanField(default=False, verbose_name="El producto se encuentra en preventa")
    imagen = models.ImageField(upload_to="cajas/",  blank=True, null=True, verbose_name="Imagen de la caja")

    def __str__(self):
        return self.nombre
      

class ProductoCartaYugioh(models.Model):
    Rarezas = [
        ('comun', 'Común'),
        ('rara', 'Rara'),
        ('super', 'Super rara'),
        ('ultra', 'Ultra rara'),
        ('secreta', 'Secreta')
    ]

    carta = models.ForeignKey(CartaYugioh, verbose_name="Carta", on_delete=models.PROTECT, related_name="productos")
    caja = models.ForeignKey(cajaYugioh, verbose_name="Caja", on_delete=models.PROTECT)
    precio = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False, verbose_name="Precio del producto")
    stock = models.IntegerField(blank=False, null=False, verbose_name="Cantidad de existencias")
    rareza = models.CharField(choices=Rarezas, blank=False, null=False, max_length=20, verbose_name="Rareza de la carta")
    imagen = models.ImageField(upload_to="cartas/", blank=True, null=True, verbose_name="Imagen de la carta")

    def __str__(self):
        return f"{self.carta.nombre} - {self.caja.nombre} - {self.rareza}"
        
    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.delete(save=False)
        super().delete(using=using, keep_parents=keep_parents)


class cartaMagic(Carta):
    juego = models.CharField(default='Magic: The Gathering', max_length=50, verbose_name="Juego de cartas")

    def __str__(self):
        return self.nombre

class cajaMagic(Caja):
    stock = models.IntegerField(blank=False, null=False, verbose_name="Cantidad en existencias")
    precio = models.DecimalField(blank=False, null=False, verbose_name="Precio del producto", decimal_places=2, max_digits=6)
    preventa = models.BooleanField(default=False, verbose_name="El producto se encuentra en preventa")
    imagen = models.ImageField(upload_to="cajas/",  blank=True, null=True, verbose_name="Imagen de la caja")

    def __str__(self):
        return self.nombre


class ProductoCartaMagic(models.Model):
    Rarezas = [
        ('Rara Mitica', 'Rara Mitica'),
        ('Rara', 'Rara'),
        ('Infrecuente', 'Infrecuente'),
        ('Común', 'Común'),
        ('Tierra básica', 'Tierra básica'),
        ('Token','Token')
    ]

    carta = models.ForeignKey(cartaMagic, verbose_name="Carta", on_delete=models.PROTECT)
    caja = models.ForeignKey(cajaMagic, verbose_name="Caja", on_delete=models.PROTECT)
    precio = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False, verbose_name="Precio del producto")
    stock = models.IntegerField(blank=False, null=False, verbose_name="Cantidad de existencias")
    rareza = models.CharField(choices=Rarezas, blank=False, null=False, max_length=20, verbose_name="Rareza de la carta")
    imagen = models.ImageField(upload_to="cartas/", blank=True, null=True, verbose_name="Imagen de la carta")

    def __str__(self):
        return f"{self.carta.nombre} - {self.caja.nombre} - {self.rareza}"
        
    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.delete(save=False)
        super().delete(using=using, keep_parents=keep_parents)


class Venta(models.Model):
    ESTADO_OPCIONES = [
        ('PROCESANDO', 'Procesando'),
        ('ENVIADO', 'Enviado'),
        ('COMPLETADO', 'Completado'),
        ('REEMBOLSADO', 'Reembolsado'),
        ('FALLIDO', 'Fallido'),
    ]

    usuario = models.ForeignKey(Usuario, verbose_name="usuario", on_delete=models.PROTECT)
    fecha = models.DateField(auto_now_add=True) 
    total = models.DecimalField(decimal_places=2, max_digits=10)
    estado = models.CharField(choices=ESTADO_OPCIONES, max_length=50)  

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha} - {self.get_estado_display()}"


class VentaDetalle(models.Model):
    JUEGO = [
        ('Yu-Gi-Oh!', 'Yu-Gi-Oh!'),
        ('Magic: The Gathering', 'Magic: The Gathering')
    ]

    venta = models.ForeignKey(Venta, verbose_name="Id de la venta", on_delete=models.PROTECT)
    producto = models.CharField(verbose_name="Producto", max_length=50)
    precio_unitario = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False, verbose_name="Precio del producto", default=0)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    precio_total = models.DecimalField(verbose_name="Total", max_digits=10, decimal_places=2)
    juego = models.CharField(verbose_name="TCG", choices=JUEGO, max_length=50)

    def __str__(self):
        return f"{self.venta} - {self.producto} - {self.cantidad} - ${self.precio_total}"







    
    
    
    

