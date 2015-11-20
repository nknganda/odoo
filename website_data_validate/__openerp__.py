# -*- coding: utf-8 -*-
{
    'name': "e-Commerce -> User 'Checkout' Information Validator",

    'summary': """
        Save time and resources by validating the info entered by your online customer before he or she submits them. Quickly validate billing & shipping information as the user is typing them in. No need to submit wrong information empty data then ask the customer to type them in again
        """,

    'description': """
        This Modules ensures that the data entered by your customer is valid before submitting to the ecommerce backend. 
	Information entered by online customer such as email, phone, billing address, shipping/delivery address are validated before submitting
	The messages returned to the form when invalid data is entered can be customised easilt to suit your preference. 
	Also the messages are translated to any language used in the website
    """,

    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",
    'images': ['static/description/main2.png'],
    'price': 15,
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
