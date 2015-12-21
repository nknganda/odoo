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
    'depends': ['base', 'sale', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/sale_order_reports.xml',
        'reports/purchase_order_reports.xml',
        'reports/rfq_reports.xml',

        'sale_order/all_reports.xml',
        'sale_order/sale_order_view.xml',
        'sale_order/res_company_view.xml',
        'sale_order/odoo_template.xml',
        'sale_order/retro_template.xml',
        'sale_order/classic_template.xml',
        'sale_order/tva_template.xml',
        'sale_order/modern_template.xml',

        'purchase_order/all_reports.xml',
        'purchase_order/purchase_order_view.xml',
        'purchase_order/res_company_view.xml',
        'purchase_order/odoo_template.xml',
        'purchase_order/retro_template.xml',
        'purchase_order/classic_template.xml',
        'purchase_order/tva_template.xml',
        'purchase_order/modern_template.xml',


        'rfq/all_reports.xml',
        'rfq/rfq_view.xml',
        'rfq/res_company_view.xml',
        'rfq/odoo_template.xml',
        'rfq/retro_template.xml',
        'rfq/classic_template.xml',
        'rfq/tva_template.xml',
        'rfq/modern_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}
