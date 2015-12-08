# -*- coding: utf-8 -*-
{
    'name': "e-Commerce Checkout Data Verification",

    'summary': """
        Save time and resources by validating the info entered by your online customer before he or she submits them for processing.
        """,

    'description': """
    """,

    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",
    'images': ['static/description/data.png'],
    'price': 12,
    'currency': 'EUR',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_jquery_validation'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/validation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
