# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class account_mobile_money_company(models.Model):
	_inherit = "res.company"

	mobilem_create_payment = fields.Boolean('Create a payment entry in odoo for every successful Mobile Money transaction', default=False)
	mobilem_create_invoice = fields.Boolean('Create and validate invoice in odoo for every successful Mobile Money transaction', default=False)
	mobilem_send_invoice = fields.Boolean('Send Invoice to customer after every successful Mobile Money transaction', default=False)
	mobilem_register_payment = fields.Boolean('Automatically reconcile a payment with an invoice when both are created by Mobile Money', default=False)

		
class account_mobile_money_config(models.TransientModel):
      	_inherit = 'account.config.settings'

	module_payment_mobilem = fields.Boolean('Mobile Money (Mobilem)', help='-check/uncheck to install/un-install the Mobile Money Module')
	mobilem_create_payment = fields.Boolean(related='company_id.mobilem_create_payment')
	mobilem_create_invoice = fields.Boolean(related='company_id.mobilem_create_invoice')
	mobilem_send_invoice = fields.Boolean(related='company_id.mobilem_send_invoice')
	mobilem_register_payment = fields.Boolean(related='company_id.mobilem_register_payment')


	@api.one
	@api.onchange('mobilem_register_payment')
	def onchange_mobilem_register_payment(self):
		if self.mobilem_register_payment == True:
		   self. mobilem_create_invoice = True
		   self. mobilem_create_payment = True

	@api.one
	@api.onchange('mobilem_send_invoice')
	def onchange_mobilem_send_invoice(self):
		if self.mobilem_send_invoice == True:
		   self. mobilem_create_invoice = True
