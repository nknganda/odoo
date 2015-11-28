# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import fields, osv
# class mpesa_payment(models.Model):
#     _name = 'mpesa_payment.mpesa_payment'

#     name = fields.Char()
class account_mobile_money_config(osv.TransientModel):
      _inherit = 'account.config.settings'

      _columns = {
        'module_payment_mobilem': fields.boolean('Mobile Money (Mobilem)', help='-check/uncheck to install/un-install the Mobile Money Module'),
      }
class Mobilem_configs(models.Model):
	_inherit = 'account.config.settings'

	mobilem_create_payment = fiels.Boolean('Create Payment in odoo from every successful Mobile Payment Transaction', default=False)
