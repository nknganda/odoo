# -*- coding: utf-8 -*-
{
    'name': "HR for Kenya ",

    'summary': """
        Kenya Specific HR details for Employees, Employers and Contracts""",

    'description': """
        In this module, we are adding Kenya specific HR details and requirements for processing payroll. NSSF, NHIF, Next Of Kin, PAYE, HELB and others
    """,

    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",
    'price': 400,
    'currency': 'USD',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_contract', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
	'data.xml',
        'hr.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
