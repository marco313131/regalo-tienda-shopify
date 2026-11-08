# El diseño de la tienda del video

Es el diseño de la tienda de nieve del video «Cómo conectar Claude a tu tienda de Shopify (sin copiar y pegar código)». Trae:
- los colores y las letras;
- la portada con foto;
- la marquesina;
- el carrusel de productos;
- los dos bloques con foto;
- las secciones que aparecen al bajar.

Va sobre **Horizon**, el tema gratis de Shopify. Esta carpeta no trae una copia del tema: trae el diseño, y se aplica sobre tu propio Horizon.

## Qué necesitás

- **Tu tienda con el tema Horizon.** Las tiendas nuevas ya lo traen. Si la tuya no lo tiene, agregalo desde Tienda online › Temas › Agregar tema.
- **Tu tema conectado con GitHub y con la pestaña Code de Claude**, como en el video.

## Cómo se aplica

1. **Bajá esta carpeta:** arriba, botón verde «Code» › «Download ZIP». Descomprimila y poné la carpeta `regalo-tienda-shopify` adentro de la carpeta de tu tema.
2. **Subí las tres fotos de `fotos/`** a tu tienda, en Contenido › Archivos, sin cambiarles el nombre. El diseño las busca por ese nombre.
3. **En la pestaña Code de Claude, pegá este pedido:**

   > Aplicá el diseño de la carpeta regalo-tienda-shopify: corré `python3 regalo-tienda-shopify/aplicar-diseno.py .` en la carpeta del tema. Si no hay Python, leé ese archivo y hacé vos los mismos cambios en esos 4 archivos. Si algo no coincide con mi versión de Horizon, ajustalo sin tocar nada más. Después sacá la carpeta regalo-tienda-shopify del tema, hacé commit y push.

4. **Refrescá tu tienda.**

## Después

- **Los productos.** El carrusel y el producto destacado apuntan a una colección y a un producto de la tienda de prueba. En el editor de temas, elegí los tuyos.
- **Los textos.** Cambiá los de la portada, la marquesina y la barra de arriba por los de tu tienda. También se lo podés pedir a Claude.

Lo que cambia son solo 4 archivos de tu tema:
- `config/settings_data.json`
- `sections/header-group.json`
- `templates/index.json`
- `sections/footer-group.json`

Si no te gusta, volvé al commit anterior desde GitHub Desktop.

Canal: https://www.youtube.com/@Sociobot-ia
