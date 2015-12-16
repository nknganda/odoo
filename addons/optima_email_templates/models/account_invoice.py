from openerp import SUPERUSER_ID
from openerp import api, models, _


class accountInvoice(models.Model):

	_inherit = 'account.invoice'
	
	@api.one
	def get_login_url(self):
	    return '' + self.env['ir.config_parameter'].get_param('web.base.url') + '/my/home'
