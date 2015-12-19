# -*- coding: utf-8 -*-
{
    'name': "Professional PO/RFQ/SO/SQ/D Note/Pickling List",

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
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/reports.xml',
        'views/all_reports.xml',
        'views/sale_order_view.xml',
        'views/res_company_view.xml',
        'views/odoo_sale_order.xml',
        'views/retro_template.xml',
        'views/classic_template.xml',
        'views/modern_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}
