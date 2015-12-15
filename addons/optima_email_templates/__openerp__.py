# -*- coding: utf-8 -*-
{
    'name': "Installs Email Templates for Optima ICT",

    'summary': """
        This Module installs email templates for Invoice, sales order and admin Signature""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'portal_sale', 'website_quote'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/email_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    #    'demo.xml',
    ],
}
