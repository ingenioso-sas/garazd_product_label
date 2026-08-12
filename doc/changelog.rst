.. _changelog:

Changelog
=========

`13.0.1.13.0`
--------

- [ADD] Procesamiento por lotes en la impresion de etiquetas: se configura el tamano del lote desde Ajustes (Product Labels / Label batch size). Al imprimir muchas etiquetas, el PDF se genera por lotes mas pequenos y se unen, limitando el consumo de RAM/CPU en contenedores con recursos limitados. Valor 0 = comportamiento anterior (un solo render).
- [FIX] Se elimina el dict unpacking (`{**...}`) en los templates QWeb, que esta prohibido por el safe_eval de Odoo 13. El costo en codigo se calcula una vez por producto sin usar diccionarios.

`13.0.1.12.0`
--------

- [PERF] Se cachea el resultado de `get_cost_in_code()` por producto en las etiquetas 25x25 y 58x32. Antes se ejecutaban 2 consultas SQL por etiqueta (1000 etiquetas = 2000 consultas); ahora solo 1 por producto distinto. Acelera la generacion del HTML al imprimir muchas etiquetas del mismo producto.

`13.0.1.11.0`
--------

- [FIX] Temporal: el codigo de barras vuelve a generarse por URL (`/report/barcode/...`) con `web_base_url` absoluto en las tres etiquetas (25x25, 58x32 y 57x35 A4), en lugar del widget base64, para reducir el consumo de memoria de wkhtmltopdf al imprimir muchas etiquetas en contenedores con limite de memoria bajo (p. ej. 800MB). El widget base64 se restaura cuando se resuelva el limite de memoria del contenedor.

`13.0.1.10.0`
--------

- [IMP] Se unifica el esquema de las etiquetas 58x32mm y 57x35mm (A4) con el de la 25x25mm: escalado automatico de letra con `font_scale`, parametros configurables (margen, rejilla, ancho/alto de codigo de barras), codigo de barras embebido en base64 via widget QWeb, y margenes de paperformat a 0 (el margen se controla por parametro).
- [ADD] La rejilla (columnas/filas) ahora tambien es configurable para la etiqueta 58x32mm.
- [I18N] Se actualizan el archivo `.pot` y la traduccion al espanol con las nuevas cadenas.

`13.0.1.9.1`
--------

- [ADD] Rejilla configurable tambien para la etiqueta 25x25mm (porcentajes, default 1x1 = comportamiento anterior). Los campos Columns/Rows se muestran para A4 y 25x25, y cambian de default al seleccionar el template (A4: 3x7, otros: 1x1).

`13.0.1.9.0`
--------

- [ADD] Rejilla A4 personalizable (filas/columnas) desde la vista de impresion (porcentajes, sin dimensionado exacto). Default 3x7 como antes.

`13.0.1.4.0`
--------

- [FIX] Se agrega el reporte de preview para la plantilla A4 (57x35mm).
- [FIX] Se filtran las lineas de orden de compra sin producto o con cantidad cero.
- [FIX] Se corrigen los codigos de barras de 8 digitos en la etiqueta 25x25 (duplicacion de imagen EAN13/EAN8).
- [FIX] Se generan etiquetas para todas las variantes de un `product.template`.
- [FIX] Se reemplaza la excepcion deprecada `Warning` por `UserError`.
- [IMP] Se refactoriza `_get_products` para devolver comandos `(0, 0, ...)` en lugar de crear registros sueltos, con soporte de `active_ids` y mensaje de error claro.
- [IMP] Se reutiliza la plantilla `label_57x35_a4` en el reporte A4 (se elimina el codigo duplicado) y se corrige el salto de pagina inicial.
- [IMP] Se eliminan campos, bloques y divs sin uso (`message`, `output`, divs vacios).
- [IMP] Se elimina `default=True` de los tres `report.paperformat`.

`13.0.1.0.1`
-------

- Init version
