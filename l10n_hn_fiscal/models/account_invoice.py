# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    @api.one
    @api.depends('amount_total')
    def get_amount_in_words(self):
        self.amount_in_words = self.currency_id.amount_to_text(self.amount_total) + " ***"
    
    amount_in_words = fields.Char(string="Monto en letras", readonly=True, compute='get_amount_in_words')
    cai_supplier = fields.Char(string="CAI", store=True)
    cai = fields.Char(string="CAI", store=True, readonly=True)
    emition = fields.Date('Fecha de recepcion', store=True)
    emition_limit = fields.Date('Fecha limite de emision', store=True)
    declaration = fields.Char('Declaracion', store=True)
    range_start_str = fields.Char('Correlativo Inicial', store=True)
    range_end_str = fields.Char('Correlativo Final', store=True)
    cancelled_invoice = fields.Char('Factura Cancelada', readonly=True)
    num_contract_exonerated = fields.Char('Constancia resgistro exonerada')
    num_contract_sag = fields.Char('Registro SAG')
    num_exempt_purchase = fields.Char('Orden de compra exenta')

    global_discount = fields.Monetary('Descuento',compute='_compute_taxess')
    global_exonerated = fields.Monetary('Exonerado',compute='_compute_taxess')
    global_exempt = fields.Monetary('Exento',compute='_compute_taxess')
    global_tax_15 = fields.Monetary('Isv 15%',compute='_compute_taxess')
    global_tax_18 = fields.Monetary('Isv 18%',compute='_compute_taxess')
    

    @api.multi
    def invoice_validate(self):
        for invoice in self.filtered(lambda invoice: invoice.partner_id not in invoice.message_partner_ids):
            invoice.message_subscribe([invoice.partner_id.id])
        self._check_duplicate_supplier_reference()

        if self.journal_id.sequence_id.cai:
            if self.date_invoice > self.journal_id.sequence_id.emition_limit:
                self.journal_id.sequence_id.number_next_actual = self.journal_id.sequence_id.number_next_actual -1
                raise Warning(_('la fecha de expiracion para este documento es %s ') %(self.journal_id.sequence_id.emition_limit) )

            if self.journal_id.sequence_id.number_next_actual == self.journal_id.sequence_id.range_end:
                self.journal_id.sequence_id.number_next_actual = self.journal_id.sequence_id.number_next_actual -1
                raise Warning(_('En correlativo fiscal final para este documento es %s ') %(self.journal_id.sequence_id.range_end) )

            for fiscal in self.journal_id.sequence_id:
                if fiscal.active_sar == True:
                    self.cai = fiscal.cai
                    self.emition = fiscal.emition
                    self.emition_limit = fiscal.emition_limit
                    self.declaration = fiscal.declaration
                    self.range_end_str = fiscal.range_end_str
                    self.range_start_str = fiscal.range_start_str
                    self.cancelled_invoice = self.number
                    self.write({'state': 'open'})

        return super(AccountInvoice, self).invoice_validate()


    @api.one
    @api.depends('invoice_line_ids.discount_line', 'invoice_line_ids.exonerated_line','invoice_line_ids.exempt_line', 'invoice_line_ids.tax_15_line')
    def _compute_taxess(self):
        self.global_discount = sum(line.discount_line for line in self.invoice_line_ids)
        self.global_exempt = sum(line.exempt_line for line in self.invoice_line_ids)
        self.global_tax_15 = sum(line.tax_15_line for line in self.invoice_line_ids)
        self.global_tax_18 = sum(line.tax_18_line for line in self.invoice_line_ids)
        self.global_exonerated = sum(line.exonerated_line for line in self.invoice_line_ids)

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    discount_line = fields.Monetary('Descuento', compute='_compute_discount')
    exonerated_line = fields.Monetary('Exonerado', compute ='_compute_sar_line')
    exempt_line = fields.Monetary('Exento', compute ='_compute_sar_line')
    tax_15_line = fields.Monetary('Isv 15%', compute ='_compute_sar_line')
    tax_18_line = fields.Monetary('Isv 18%', compute ='_compute_sar_line')

    @api.one
    @api.depends('discount', 'quantity', 'price_unit')
    def _compute_discount(self):
        self.discount_line = (self.price_unit * self.quantity) * (self.discount / 100)

    @api.one
    @api.depends('invoice_line_tax_ids', 'invoice_line_tax_ids.name', 'price_unit', 'quantity','price_subtotal','discount_line')
    def _compute_sar_line(self):
        for rec in self.invoice_line_tax_ids:
            if rec.name == "EXE":
                self.exempt_line = self.quantity * self.price_unit
            if rec.name == "ISV15":
                self.tax_15_line = ((self.quantity * self.price_unit) - self.discount_line) - self.price_subtotal
            if rec.name == "ISV18":
                self.tax_18_line = ((self.quantity * self.price_unit) - self.discount_line) - self.price_subtotal
            if rec.name == "EXO":
                self.exonerated_line = self.quantity * self.price_unit
