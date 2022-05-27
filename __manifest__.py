# Copyright © 2018 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Custom Product Labels',
    'version': '15.0.1.0.1',
    'category': 'Warehouse',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz',
    'license': 'LGPL-3',
    'summary': 'Print custom product labels with barcode',
    'images': ['static/description/banner.png'],
    'description': """
        Module allows to print custom product barcode labels and tags on different paper formats.
        This module include the one label template with size: 57x35mm, paperformat: 21 pcs per sheet, 57 x 32 cm.
    """,
    'depends': ['product', 'customized_barcode_generator'],
    'data': [
        'wizard/print_product_label_views.xml',
        'report/product_label_templates.xml',
        'report/product_label_templates_a4.xml',
        'report/product_label_templates_25x25.xml',
        'report/product_label_reports.xml',
        'report/product_label_reports_a4.xml',
        'report/product_label_reports_25x25.xml',
    ],
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
