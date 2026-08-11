# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

SUPPORTED_MODELS = ('product.template', 'product.product', 'purchase.order')


class PrintProductLabel(models.TransientModel):
    _name = "print.product.label"
    _description = 'Product Labels Wizard'

    @api.model
    def _get_products(self):
        label_lines = []

        active_model = self._context.get('active_model')
        record_ids = self._context.get('active_ids') or self._context.get('default_product_ids')

        if active_model not in SUPPORTED_MODELS:
            raise UserError(
                _('Printing product labels is only supported from products and purchase orders.')
            )

        records = self.env[active_model].browse(record_ids)

        if active_model == 'product.template':
            for template in records:
                for product in template.product_variant_ids:
                    label_lines.append((0, 0, {'product_id': product.id}))
        elif active_model == 'product.product':
            for product in records:
                label_lines.append((0, 0, {'product_id': product.id}))
        elif active_model == 'purchase.order':
            for order in records:
                for line in order.order_line.filtered(
                        lambda line: line.product_id and line.product_qty > 0):
                    label_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'qty_initial': line.product_qty,
                        'qty': line.product_qty,
                    }))

        return label_lines

    label_ids = fields.One2many(
        comodel_name='print.product.label.line',
        inverse_name='wizard_id',
        string='Labels for Products',
        default=_get_products,
    )
    template = fields.Selection(
        selection=[
            ('garazd_product_label.report_product_label_A4_57x35', 'Label 57x35mm (A4: 21 pcs on sheet, 3x7)'),
            ('garazd_product_label.report_product_label_custom_58x32', 'Label 58x32mm (custom: 1 pcs on sheet, 1x1)'),
            ('garazd_product_label.report_product_label_custom_25x25', 'Label 25x25mm (custom: 1 pcs on sheet, 1x1)')
        ],
        string='Label template',
        default='garazd_product_label.report_product_label_custom_58x32',
    )
    qty_per_product = fields.Integer(
        string='Label quantity per product',
        default=1,
    )
    columns = fields.Integer(
        string='Grid columns',
        default=1,
        help="Number of label columns on the sheet (e.g. A4: 3).",
    )
    rows = fields.Integer(
        string='Grid rows',
        default=1,
        help="Number of label rows on the sheet (e.g. A4: 7).",
    )
    barcode_width = fields.Integer(
        string='Barcode Width (px)',
        default=600,
        help="Width of the generated barcode image in pixels.",
    )
    barcode_height = fields.Integer(
        string='Barcode Height (px)',
        default=180,
        help="Height of the generated barcode image in pixels.",
    )

    @api.onchange('template')
    def _onchange_template_grid(self):
        if self.template == 'garazd_product_label.report_product_label_A4_57x35':
            self.columns = 3
            self.rows = 7
        else:
            self.columns = 1
            self.rows = 1

    @api.constrains('columns', 'rows')
    def _check_grid(self):
        for record in self:
            if record.columns < 1 or record.rows < 1:
                raise ValidationError(_('Grid columns and rows must be at least 1.'))

    def _get_print_data(self):
        """Pass grid configuration for the grid reports (A4 and 25x25)."""
        self.ensure_one()
        data = {
            'barcode_width': self.barcode_width or 600,
            'barcode_height': self.barcode_height or 180,
        }
        if self.template in (
                'garazd_product_label.report_product_label_A4_57x35',
                'garazd_product_label.report_product_label_custom_25x25'):
            data.update({'columns': self.columns, 'rows': self.rows})
        return data

    def action_print(self):
        """ Print labels """
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')
        if not labels:
            raise UserError(_('Nothing to print, set the quantity of labels in the table.'))
        return self.env.ref(self.template).with_context(
            discard_logo_check=True).report_action(labels, data=self._get_print_data())

    def action_set_qty(self):
        self.ensure_one()
        self.label_ids.write({'qty': self.qty_per_product})

    def action_restore_initial_qty(self):
        self.ensure_one()
        for label in self.label_ids.filtered('qty_initial'):
            label.qty = label.qty_initial

    def action_set_product_available_qty(self):
        for label in self.label_ids:
            if label.product_id:
                label.qty = max(0, int(label.product_id.free_qty or 0))

    def action_preview(self):
        """ Preview labels """
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')
        if not labels:
            raise UserError(_('Nothing to preview, set the quantity of labels in the table.'))
        return self.env.ref('%s_preview' % self.template).with_context(
            discard_logo_check=True).report_action(labels, data=self._get_print_data())
