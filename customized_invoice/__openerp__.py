# -*- coding: utf-8 -*-
{
    'name': "Professional Invoice Templates - Odoo9.0",

    'summary': """
        Make your Invoice reports look professional by branding them. Choose from three professional Invoice templates and unlimited colors """,

    'description': """
        This module will install a customized client invoice report for accounting module.You will be able to customize the invoice colors,logo and the style/format of invoice to look professional and appealing to your customers. You can also create your own template from scratch or edit one of the existing templates that come with this module 
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
        'views/tva_template.xml',
        'views/account_invoice_view.xml',
        'views/res_company_view.xml',
        'reports/reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
