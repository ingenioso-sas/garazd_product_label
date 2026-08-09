.. _changelog:

Changelog
=========

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
