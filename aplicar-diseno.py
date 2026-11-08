#!/usr/bin/env python3
"""El diseño de la tienda de nieve del video, aplicado sobre tu propio tema Horizon.
Cambia 4 archivos de la carpeta de tu tema y nada más: config/settings_data.json, sections/header-group.json,
templates/index.json y sections/footer-group.json. Necesita animaciones.liquid al lado de este archivo.
Uso, parado en la carpeta de tu tema: python3 regalo-tienda-shopify/aplicar-diseno.py ."""
import json, re, sys, pathlib

SAL = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
if not (SAL / 'config/settings_schema.json').exists():
    raise SystemExit('Esta no es la carpeta de un tema de Shopify: no encuentro config/settings_schema.json')

COMENTARIO = re.compile(r'^\s*/\*.*?\*/\s*', re.S)

def leer(rel):
    t = (SAL / rel).read_text(encoding='utf-8')
    m = COMENTARIO.match(t)
    cab = m.group(0) if m else ''
    return cab, json.loads(t[len(cab):])

def escribir(rel, cab, d):
    (SAL / rel).write_text(cab + json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def esquema(rel):
    t = (SAL / rel).read_text(encoding='utf-8')
    return json.loads(re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}', t, re.S).group(1))

# ---------- control: cada select con un valor que exista ----------
def opciones(settings):
    return {s['id']: [o['value'] for o in s.get('options', [])] for s in settings if s.get('id') and s.get('type') == 'select'}

def controlar(nombre, valores, settings):
    ops = opciones(settings)
    rangos = {s['id']: (s.get('min'), s.get('max')) for s in settings if s.get('id') and s.get('type') == 'range'}
    for k, v in valores.items():
        if k in rangos and isinstance(v, (int, float)) and not (rangos[k][0] <= v <= rangos[k][1]):
            raise SystemExit(f'{nombre}: {k}={v} fuera de {rangos[k]}')
        if k in ops and ops[k] and v not in ops[k]:
            raise SystemExit(f'{nombre}: {k}={v!r} no está en {ops[k]}')

TEMA = json.loads((SAL / 'config/settings_schema.json').read_text(encoding='utf-8'))
TEMA_SETTINGS = [s for g in TEMA for s in g.get('settings', [])]

# ---------- 1. Ajustes del tema ----------
cab, data = leer('config/settings_data.json')
c = data['current']
NAVY, NAVY2, HIELO, BORDE = '#0B1F33', '#1E3A5C', '#EAF2F8', '#D9E3EC'
c['color_palette'] = {'background': '#FFFFFF', 'foreground': NAVY, 'color1': NAVY2, 'color2': BORDE}
nuevos = {
    'type_heading_font': 'montserrat_n8', 'type_accent_font': 'montserrat_n7',
    'type_body_font': 'inter_n4', 'type_subheading_font': 'inter_n6',
    'type_size_paragraph': '16', 'type_line_height_paragraph': 'body-normal',
    'type_size_h1': '72', 'type_case_h1': 'uppercase', 'type_letter_spacing_h1': 'heading-tight', 'type_line_height_h1': 'display-tight',
    'type_size_h2': '48', 'type_case_h2': 'uppercase', 'type_letter_spacing_h2': 'heading-tight', 'type_line_height_h2': 'display-tight',
    'type_size_h3': '32', 'type_letter_spacing_h3': 'heading-tight',
    'type_case_h6': 'uppercase', 'type_letter_spacing_h6': 'heading-loose',
    'page_width': 'normal',
    'page_transition_enabled': True, 'transition_to_main_product': True, 'add_to_cart_animation': True,
    'card_hover_effect': 'lift',
    'button_border_radius_primary': 100, 'button_border_radius_secondary': 100,
    'button_text_case_primary': 'uppercase', 'button_text_case_secondary': 'uppercase',
    'type_font_button_primary': 'accent', 'type_font_button_secondary': 'accent',
    'primary_button_border_width': 0, 'secondary_button_border_width': 2,
    'product_corner_radius': 14, 'card_corner_radius': 14,
    'badge_corner_radius': 100, 'badge_text_transform': 'uppercase',
    'inputs_border_radius': 32,
}
controlar('settings_data', nuevos, TEMA_SETTINGS)
c.update(nuevos)
escribir('config/settings_data.json', cab, data)

# ---------- 2. Barra de anuncios y encabezado ----------
cab, hg = leer('sections/header-group.json')
ann = hg['sections']['header_announcements_9jGBFp']
blk = ann['blocks']['announcement_BxgCk9']['settings']
blk['text'] = 'Nueva temporada: tablas y ceras para la montaña'
blk['text_color'] = NAVY
ann['settings']['background_color'] = HIELO
ann['settings']['divider_width'] = 0
hdr = hg['sections']['header_section']['settings']
hdr['enable_transparent_header_home'] = True
hdr['text_color_transparent_home'] = '#FFFFFF'
escribir('sections/header-group.json', cab, hg)

# ---------- 3. Portada ----------
cab, idx = leer('templates/index.json')
S = idx['sections']

def texto(t, preset, **extra):
    s = {'text': t, 'type_preset': preset, 'width': '100%', 'max_width': 'normal', 'alignment': 'left', 'wrap': 'pretty'}
    s.update(extra)
    return {'type': 'text', 'settings': s, 'blocks': {}}

def boton(label, link, estilo='button', **extra):
    s = {'label': label, 'link': link, 'style_class': estilo}
    s.update(extra)
    return {'type': 'button', 'settings': s, 'blocks': {}}

BLANCO = '#FFFFFF'
hero = {
    'type': 'hero',
    'blocks': {
        'cap': texto('<p>Temporada 2026 · Patagonia</p>', 'h6', text_color=BLANCO, max_width='narrow'),
        'tit': texto('<h1>Hecho para la nieve</h1>', 'h1', text_color=BLANCO, max_width='narrow'),
        'bajada': texto('<p>Tablas y ceras elegidas para bajar la montaña con todo, desde tu primera bajada hasta la más difícil.</p>', 'rte', text_color=BLANCO, max_width='narrow', **{'padding-block-end': 16}),
        'btn': boton('Ver la colección', 'shopify://collections/all', 'button-custom',
                     custom_button_background=BLANCO, custom_button_text=NAVY, custom_button_border=BLANCO),
    },
    'block_order': ['cap', 'tit', 'bajada', 'btn'],
    'settings': {
        'media_type_1': 'image', 'image_1': 'shopify://shop_images/portada-nieve.jpg',
        'content_direction': 'column', 'vertical_on_mobile': True,
        'horizontal_alignment_flex_direction_column': 'flex-start',
        'vertical_alignment_flex_direction_column': 'flex-end',
        'gap': 14, 'section_width': 'page-width', 'section_height': 'full-screen',
        'toggle_overlay': True, 'overlay_color': '#0B1F33C7', 'overlay_style': 'gradient', 'gradient_direction': 'to top',
        'padding-block-start': 72, 'padding-block-end': 72,
    },
}
controlar('hero', hero['settings'], esquema('sections/hero.liquid')['settings'])

frases = ['Nueva temporada', 'Tablas para todos los niveles', 'Ceras para cada tipo de nieve', 'Hecho para la montaña']
mq_blocks, mq_order = {}, []
for i, f in enumerate(frases):
    for k, t in ((f'f{i}', f), (f's{i}', '✦')):
        mq_blocks[k] = texto(f'<p>{t}</p>', 'h3', text_color=BLANCO, case='uppercase', wrap='nowrap', width='fit-content')
        mq_order.append(k)
marquesina = {'type': 'marquee', 'blocks': mq_blocks, 'block_order': mq_order,
              'settings': {'movement_direction': 'normal', 'background_color': NAVY,
                           'padding-block-start': 22, 'padding-block-end': 22, 'gap_between_elements': 28}}

lista = S['product_list_fa6P9H']
cambios = []
def recorrer(n):
    if isinstance(n, dict):
        for k, v in n.items():
            if k == 'text' and isinstance(v, str) and 'closest.collection.title' in v:
                n[k] = '<h2>Lo más elegido</h2>'; cambios.append('titulo lista')
            elif k == 'label' and v in ('View all', 'Shop all'):
                n[k] = 'Ver todo'; cambios.append('ver todo')
            else:
                recorrer(v)
    elif isinstance(n, list):
        for x in n: recorrer(x)
recorrer(lista)
lista['settings'].update({'collection': 'automated-collection', 'layout_type': 'carousel', 'max_products': 6, 'columns': 4, 'carousel_on_mobile': True, 'rows_gap': 36, 'columns_gap': 16, 'padding-block-start': 80, 'padding-block-end': 80})

def editorial(img, lado, fondo, cap, tit, txt, label, link='shopify://collections/all'):
    return {
        'type': 'media-with-content',
        'blocks': {
            'media': {'type': '_media-without-appearance', 'static': True,
                      'settings': {'media_type': 'image', 'image': f'shopify://shop_images/{img}', 'image_position': 'cover'}, 'blocks': {}},
            'content': {'type': '_content-without-appearance', 'static': True,
                        'settings': {'horizontal_alignment_flex_direction_column': 'flex-start',
                                     'vertical_alignment_flex_direction_column': 'center', 'gap': 20},
                        'blocks': {'cap': texto(f'<p>{cap}</p>', 'h6', text_color=NAVY2),
                                   'tit': texto(f'<h2>{tit}</h2>', 'h2', max_width='narrow'),
                                   'txt': texto(f'<p>{txt}</p>', 'rte', max_width='narrow'),
                                   'btn': boton(label, link)},
                        'block_order': ['cap', 'tit', 'txt', 'btn']},
        },
        'settings': {'media_position': lado, 'media_width': 'medium', 'media_height': '80svh',
                     'section_width': 'full-width', 'extend_media': True, 'background_color': fondo,
                     'padding-block-start': 0, 'padding-block-end': 0},
    }

ed1 = editorial('cabana-nieve.jpg', 'left', HIELO, 'Hecho para la montaña', 'Encontrá tu tabla',
                'Freestyle, all mountain o powder: elegí la que va con tu forma de bajar y salí a la nieve con confianza.', 'Ver tablas', 'shopify://collections/automated-collection')
ed2 = editorial('detalle-nieve.jpg', 'right', '#FFFFFF', 'Cuidá tu equipo', 'Una buena cera cambia la bajada',
                'Encerá tu tabla antes de salir y deslizá más con menos esfuerzo, haga frío o calor.', 'Ver la cera', 'shopify://products/selling-plans-ski-wax')
for e in (ed1, ed2):
    controlar('media-with-content', e['settings'], esquema('sections/media-with-content.liquid')['settings'])

ANIM = (pathlib.Path(__file__).resolve().parent / 'animaciones.liquid').read_text(encoding='utf-8')
anim = {'type': 'custom-liquid', 'settings': {'custom_liquid': ANIM, 'padding-block-start': 0, 'padding-block-end': 0}}

idx['sections'] = {'portada': hero, 'marquesina': marquesina, 'product_list_fa6P9H': lista,
                   'editorial_tablas': ed1, 'editorial_cera': ed2, 'animaciones': anim}
idx['order'] = ['portada', 'marquesina', 'product_list_fa6P9H', 'editorial_tablas', 'editorial_cera', 'animaciones']
escribir('templates/index.json', cab, idx)

# ---------- 4. Pie ----------
cab, fg = leer('sections/footer-group.json')
REEMPLAZOS = {'<h2>Join our email list</h2>': '<h2>Sumate a la lista</h2>',
              '<p>Get exclusive deals and early access to new products.</p>': '<p>Ofertas y novedades de la temporada, antes que nadie.</p>',
              'Sign up': 'Suscribirme'}
quedan = []
def pie(n):
    if isinstance(n, dict):
        for k, v in n.items():
            if isinstance(v, str) and v in REEMPLAZOS:
                n[k] = REEMPLAZOS[v]
            elif isinstance(v, str) and k in ('text', 'label', 'heading') and re.search(r'[A-Za-z]{3}', re.sub('<[^>]+>|{{.*?}}', '', v)):
                quedan.append(v)
            else:
                pie(v)
pie(fg)
escribir('sections/footer-group.json', cab, fg)

print('lista:', cambios)
print('pie, textos sin traducir:', quedan)
print('listo:', SAL)
