# -*- coding: utf-8 -*-
{
    'name': "Mobile Payment Acquirer for Odoo-9.0",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/mobile_money_config.xml',
        'views/payment_mobile_views.xml',
        'views/mobile_accounts_view.xml',
        'views/mobile_providers_view.xml',
        #'views/mobile_fields_view.xml',
        'views/regex_view.xml',
        'views/message_workflow.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
