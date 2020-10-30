# -*- coding: utf-8 -*-
from odoo import models, api, fields
import logging

logger = logging.getLogger(__name__)


class ReportGeneral(models.AbstractModel):
    _name = 'report.l10n_hn_fiscal.reporte_general_print_purchase'

    @api.model
    def get_order_by_date(self, data):
        lista = []
        purchases = self.env['account.invoice'].search([('date_invoice', '>=', data['fecha_start']),
                                                        ('date_invoice', '<=', data['fecha_end']),
                                                        ('state', '!=', 'draft')])
        # logger.error('team_id: %s', data['team'])
        for purchase in purchases:
            lista.append({'date_invoice': purchase.date_invoice,
                          'partner_id.name': purchase.partner_id.name,
                          'number': purchase.number,
                          'partner_id.vat': purchase.partner_id.vat,
                          'amount_tax': purchase.amount_tax,
                          'amount_untaxed': purchase.amount_untaxed,
                          'amount_total': purchase.amount_total,
                          'currency_id': purchase.currency_id,
                          'cancelled_invoice': purchase.cancelled_invoice,
                          'state': purchase.state,
                          'journal_id': purchase.journal_id,
                          'journal_id.name': purchase.journal_id.name,
                          'reference': purchase.reference,
                          # 'team_id': purchase.team_id,
                          'global_exempt': purchase.global_exempt,
                          'range_start_str': purchase.range_start_str,
                          'global_exonerated': purchase.global_exonerated,
                          'type': purchase.type
                          })
        return lista

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data['purchases'] = self.get_order_by_date(data)
        logger.error('Compras: %s', data['purchases'])
        return data
