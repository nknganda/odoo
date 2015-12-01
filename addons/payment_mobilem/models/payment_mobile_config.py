# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class account_mobile_money_company(models.Model):
	_inherit = "res.company"

	mobilem_create_payment = fields.Boolean('Create a payment entry in odoo for every successful Mobile Money transaction', default=False)
	mobilem_create_invoice = fields.Boolean('Create and validate invoice in odoo for every successful Mobile Money transaction', default=False)

class account_mobile_money_config(models.TransientModel):
      	_inherit = 'account.config.settings'

	module_payment_mobilem = fields.Boolean('Mobile Money (Mobilem)', help='-check/uncheck to install/un-install the Mobile Money Module')
	mobilem_create_payment = fields.Boolean(related='company_id.mobilem_create_payment')
	mobilem_create_invoice = fields.Boolean(related='company_id.mobilem_create_invoice')
