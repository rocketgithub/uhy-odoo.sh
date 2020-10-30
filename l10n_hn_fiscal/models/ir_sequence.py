# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class IrSequenceSar(models.Model):
    _inherit = "ir.sequence"

    active_sar = fields.Boolean('Documento Fiscal')
    cai = fields.Char('CAI',size=37)
    emition = fields.Date('Fecha de recepcion')
    emition_limit = fields.Date('Fecha limite de emision')
    declaration = fields.Char('Declaracion', size=8)
    range_start = fields.Integer('Numero Inicial')
    range_end = fields.Integer('Numero Final')
    range_start_str = fields.Char('Correlativo Inicial', compute='_get_range_start')
    range_end_str = fields.Char('Correlativo Final', compute='_get_range_end')

    @api.one
    def _get_range_start(self):
        if self.range_start:
            start_str = str(self.range_start)
            self.range_start_str = str(self.prefix) + start_str.zfill(8)

    @api.one
    def _get_range_end(self):
        if self.range_end:
            end_str = str(self.range_end)
            self.range_end_str = str(self.prefix) + end_str.zfill(8)
