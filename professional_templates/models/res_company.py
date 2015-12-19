# -*- coding: utf-8 -*-

from openerp import models, fields, api

class default_order_settings(models.Model):
	_inherit=["res.company"]

        @api.model
        def _default_template(self):
            def_tpl = self.env['ir.ui.view'].search([('key', 'like', 'professional_templates.template\_%\_document' ), ('type', '=', 'qweb')], 
		order='id asc', limit=1)
            return def_tpl or self.env.ref('sale.report_saleorder_document')


	invoice_logo = fields.Binary("Logo", attachment=True,
               help="This field holds the image used as logo for the any report, if non is uploaded, the company logo will be used")	
	template_order = fields.Many2one('ir.ui.view', 'Order Template', default=_default_template, 
			domain="[('type', '=', 'qweb'), ('key', 'like', 'professional_templates.template\_%\_document' )]", required=True)
	#odd = fields.Char('Odd parity Color', size=7, required=True, default="#F2F2F2", help="The background color for Odd order lines in the order")	
#	even = fields.Char('Even parity Color', size=7, required=True, default="#FFFFFF", help="The background color for Even order lines in the order" )	
#	theme_color = fields.Char('Theme Color', size=7, required=True, default="#F07C4D", help="The Main Theme color of the order. Normally this\
#			 should be one of your official company colors")	
#	text_color = fields.Char('Text Color', size=7, required=True, default="#6B6C6C", help="The Text color of the order. Normally this\
#			 should be one of your official company colors or default HTML text color")	
#	name_color = fields.Char('Company Name Color', size=7, required=True, default="#F07C4D", help="The Text color of the Company Name. Normally this\
#			 should be one of your official company colors or default HTML text color")	
#	cust_color = fields.Char('Customer Name Color', size=7, required=True, default="#F07C4D", help="The Text color of the Customer Name. Normally this\
#			 should be one of your official company colors or default HTML text color")	
#	theme_txt_color = fields.Char('Theme Text Color', size=7, required=True, default="#FFFFFF",
#			 help="The Text color of the areas bearing the theme color. Normally this should NOT be the same color as the\
#				theme color. Otherwise the text will not be visible")	
