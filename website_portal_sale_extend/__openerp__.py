# -*- coding: utf-8 -*-
{
    'name': "Columns for 'Amount Due', 'Ref' on invoice list in user portal",

    'summary': """
       Adds Columns for 'Amount Due' and 'Ref'on invoice in ecommerce user portal""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '0.1',
    'images': ['static/description/web.png'],
    'price': 9,
    'currency': 'EUR',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_portal_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
