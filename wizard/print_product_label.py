# Copyright © 2018 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models, _
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)

class PrintProductLabel(models.TransientModel):
    _name = "print.product.label"
    _description = 'Product Labels Wizard'

    @api.model
    def _get_products(self):
        res = []

        active_model = self._context.get('active_model')
        _logger.info('active_model:' + str(active_model))

        _datos = self.env[active_model].browse(self._context.get('default_product_ids'))

        if active_model == 'product.template':
            products = _datos
            for product in products:
                label = self.env['print.product.label.line'].create({
                    'product_id': product.product_variant_id.id,
                })
                res.append(label.id)
        elif active_model == 'product.product':
            products = _datos
            for product in products:
                label = self.env['print.product.label.line'].create({
                    'product_id': product.id,
                })
                res.append(label.id)
        elif active_model == "purchase.order":
            orders = _datos
            for order in orders:
                orders_line = order.order_line
                for order_line in orders_line:
                    _logger.info('order_line:' + str(order_line) + "|tipo:"+str(type(order_line)))

                    # almacenar en BD la linea a imprimir
                    label = self.env['print.product.label.line'].create({
                        'product_id': order_line.product_id.id,
                        'qty_initial': order_line.product_qty,
                        'qty': order_line.product_qty
                    })
                    res.append(label.id)

        else:
            _logger.info('_get_products else - active_model:' + str(active_model))

        return res


    name = fields.Char(
        'Name',
        default='Print product labels',
    )
    message = fields.Char(
        'Message',
        readonly=True,
    )
    output = fields.Selection(
        selection=[('pdf', 'PDF')],
        string='Print to',
        default='pdf',
    )
    label_ids = fields.One2many(
        comodel_name='print.product.label.line',
        inverse_name='wizard_id',
        string='Labels for Products',
        default=_get_products,
    )
    template = fields.Selection(
        selection=[
            ('garazd_product_label.report_product_label_A4_57x35',
             'Label 57x35mm (A4: 21 pcs on a sheet, 3x7)'), 
            ('garazd_product_label.report_product_label_custom_57x32', 
             'Label 58x32mm (custom: 1 pcs on sheet, 1x1)'),
            ],
        string='Label template',
        default='garazd_product_label.report_product_label_A4_57x35',
    )
    qty_per_product = fields.Integer(
        string='Label quantity per product',
        default=1,
    )
    # Options
    humanreadable = fields.Boolean(
        string='Human readable barcode',
        help='Print digital code of barcode.',
        default=False,
    )
    border_width = fields.Integer(
        string='Border',
        help='Border width for labels (in pixels). Set "0" for no border.'
    )

    def action_print(self):
        """ Print labels """
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')
        if not labels:
            raise Warning(_('Nothing to print, set the quantity of labels in the table.'))
        return self.env.ref(self.template).with_context(discard_logo_check=True).report_action(labels)

    def action_preview(self):
        """ Preview labels """
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')
        if not labels:
            raise Warning(_('Nothing to preview, set the quantity of labels in the table.'))
        return self.env.ref('%s_preview' % self.template).with_context(discard_logo_check=True).report_action(labels)

    def action_set_qty(self):
        self.ensure_one()
        self.label_ids.write({'qty': self.qty_per_product})


    def action_restore_initial_qty(self):
        self.ensure_one()
        for label in self.label_ids:
            if label.qty_initial:
                label.update({'qty': label.qty_initial})


    def action_set_product_available_qty(self):
        for label in self.label_ids:
            if label.product_id and label.product_id.free_qty:
                label.update({'qty': label.product_id.free_qty})    
