from django.contrib import admin
from .models import Administrador, Usuario, ProductoCartaYugioh, CartaYugioh, cajaYugioh, cartaMagic, cajaMagic,ProductoCartaMagic, Venta, VentaDetalle

admin.site.register(Administrador)
admin.site.register(Usuario)
admin.site.register(cajaYugioh)
admin.site.register(ProductoCartaYugioh)
admin.site.register(cajaMagic)
admin.site.register(ProductoCartaMagic)
admin.site.register(Venta)
admin.site.register(VentaDetalle)

# Si ya tienes este registro, no lo repitas
@admin.register(CartaYugioh)
class CartaYugiohAdmin(admin.ModelAdmin):
    exclude = ('juego',)

@admin.register(cartaMagic)
class cartaMagicAdmin(admin.ModelAdmin):
    exclude = ('juego',)


