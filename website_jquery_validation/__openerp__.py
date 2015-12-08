# -*- coding: utf-8 -*-
{
    'name': "a plugin for ecommerce customer data verification",

    'summary': """
        A plugin that works together with our "e-Commerce Checkout Data verification" module to validate billing & shipping information.
        """,

    'description': """
        This is a plugin to install jquery.validate.min.js and additional methods used to validate input data  enter by user in the ecommerce website
    """,

    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",
    'images': ['static/description/plugin.png'],
#    'price': 5,
 #   'currency': 'EUR',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/jquery_validation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
