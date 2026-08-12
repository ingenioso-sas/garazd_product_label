# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    label_batch_size = fields.Integer(
        string='Label batch size',
        default=100,
        help="Number of labels rendered per batch when printing product labels. "
             "Batching limits RAM/CPU usage by rendering several smaller PDFs "
             "and merging them. Set to 0 to print all labels in one go.",
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            label_batch_size=int(params.get_param('label_batch_size', default=100) or 100),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'label_batch_size', self.label_batch_size or 0)
