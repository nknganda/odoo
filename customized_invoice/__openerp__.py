# -*- coding: utf-8 -*-
{
    'name': "Professional Invoice Report Templates - Odoo9.0",

    'summary': """
        Make your Odoo Invoice reports look professional by branding them. Choose from Five professional Invoice templates and customize the colors  and logo on the invoice to look professional ans appealing to your customers. You can also create your own template from scratch or edit one of the existing templates that come with this module """,

    'description': """
        This module will install a customized client invoice report for accounting module.
    """,
    'images': ['static/description/howto.png'],
    'price': 57,
    'currency': 'EUR',


    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'optima_social'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_invoice.xml',
        'views/modern_template.xml',
        'views/classic_template.xml',
        'views/retro_template.xml',
        'views/account_invoice_view.xml',
        'views/res_company_view.xml',
        'reports/reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
