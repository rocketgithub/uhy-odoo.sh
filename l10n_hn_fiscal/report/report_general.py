# -*- coding: utf-8 -*-
from odoo import models, api, fields
import logging

logger = logging.getLogger(__name__)


class ReportGeneral(models.AbstractModel):
    _name = 'report.l10n_hn_fiscal.reporte_general_print'

    @api.model
    def get_order_by_date(self, data):
        lista = []
        sales = self.env['account.invoice'].search([('date_invoice', '>=', data['fecha_start'],),
                                                    ('date_invoice', '<=', data['fecha_end']),
                                                    ('state', '!=', 'draft')])
        logger.error('team_id: %s', data['team'])
        for sale in sales:
            lista.append({'date_invoice': sale.date_invoice,
                          'partner_id.name': sale.partner_id.name,
                          'partner_id.vat': sale.partner_id.vat,
                          'number': sale.number,
                          'amount_tax': sale.amount_tax,
                          'amount_untaxed': sale.amount_untaxed,
                          'amount_total': sale.amount_total,
                          'currency_id': sale.currency_id,
                          'cancelled_invoice': sale.cancelled_invoice,
                          'state': sale.state,
                          'journal_id': sale.journal_id,
                          'journal_id.name': sale.journal_id.name,
                          'team_id': sale.team_id,
                          'global_exempt': sale.global_exempt,
                          'range_start_str': sale.range_start_str,
                          'global_exonerated': sale.global_exonerated,
                          'type': sale.type
                          })
        return lista

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data['sales'] = self.get_order_by_date(data)
        logger.error('Ventas: %s', data['sales'])
        return data
