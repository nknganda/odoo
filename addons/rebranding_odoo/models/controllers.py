# -*- coding: utf-8 -*-
from openerp import http

# class RebrandingOdoo(http.Controller):
#     @http.route('/rebranding_odoo/rebranding_odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rebranding_odoo/rebranding_odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rebranding_odoo.listing', {
#             'root': '/rebranding_odoo/rebranding_odoo',
#             'objects': http.request.env['rebranding_odoo.rebranding_odoo'].search([]),
#         })

#     @http.route('/rebranding_odoo/rebranding_odoo/objects/<model("rebranding_odoo.rebranding_odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rebranding_odoo.object', {
#             'object': obj
#         })