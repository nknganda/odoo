# -*- coding: utf-8 -*-

from openerp import models, fields, api

class default_report_sett(models.Model):
	_inherit=["res.company"]

        @api.model
        def _default_so_template(self):
            def_tpl = self.env['ir.ui.view'].search([('key', 'like', 'professional_templates.SO\_%\_document' ), ('type', '=', 'qweb')], 
		order='id asc', limit=1)
            return def_tpl or self.env.ref('sale.report_saleorder_document')

        @api.model
        def _default_po_template(self):
            def_tpl = self.env['ir.ui.view'].search([('key', 'like', 'professional_templates.PO\_%\_document' ), ('type', '=', 'qweb')], 
		order='id asc', limit=1)
            return def_tpl or self.env.ref('purchase.report_purchaseorder_document')

        @api.model
        def _default_rfq_template(self):
            def_tpl = self.env['ir.ui.view'].search([('key', 'like', 'professional_templates.RFQ\_%\_document' ), ('type', '=', 'qweb')], 
		order='id asc', limit=1)
            return def_tpl or self.env.ref('purchase.report_purchasequotation_document')

        @api.model
        def _default_dn_template(self):
            def_tpl = self.env['ir.ui.view'].search([('key', 'like', 'professional_templates.DN\_%\_document' ), ('type', '=', 'qweb')], 
		order='id asc', limit=1)
            return def_tpl or self.env.ref('stock.report_delivery_document')

        @api.model
        def _default_pk_template(self):
            def_tpl = self.env['ir.ui.view'].search([('key', 'like', 'professional_templates.PICK\_%\_document' ), ('type', '=', 'qweb')], 
		order='id asc', limit=1)
            return def_tpl or self.env.ref('stock.report_picking')

	invoice_logo = fields.Binary("Logo", attachment=True,
               help="This the image used as logo for any report, if non is uploaded, the company logo will be used by default")	
	template_so = fields.Many2one('ir.ui.view', 'Default Sales Order Template', default=_default_so_template, 
			domain="[('type', '=', 'qweb'), ('key', 'like', 'professional_templates.SO\_%\_document' )]", required=True)

	template_po = fields.Many2one('ir.ui.view', 'Default Purchase Order Template', default=_default_po_template, 
			domain="[('type', '=', 'qweb'), ('key', 'like', 'professional_templates.PO\_%\_document' )]", required=True)

	template_rfq = fields.Many2one('ir.ui.view', 'Default RFQ Template', default=_default_rfq_template, 
			domain="[('type', '=', 'qweb'), ('key', 'like', 'professional_templates.RFQ\_%\_document' )]", required=True)

	template_dn = fields.Many2one('ir.ui.view', 'Default Delivery Slip Template', default=_default_dn_template, 
			domain="[('type', '=', 'qweb'), ('key', 'like', 'professional_templates.DN\_%\_document' )]", required=True)

	template_pk = fields.Many2one('ir.ui.view', 'Default Picking Template', default=_default_pk_template, 
			domain="[('type', '=', 'qweb'), ('key', 'like', 'professional_templates.PICK\_%\_document' )]", required=True)


