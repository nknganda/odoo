# -*- coding: utf-8 -*-
{
    'name': "Rebrand Odoo",

    'summary': """
        This Module rebrands  odoo 9.0 by removing instances of the word Odoo or 'Powerd by Odoo'
        """,

    'description': """
        This Module rebrands  odoo 9.0 by removing instances of the word Odoo or 'Powerd by Odoo'
    """,

    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
