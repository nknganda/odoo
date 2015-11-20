# -*- coding: utf-8 -*-
{
    'name': "e-Commerce -> Upload and Zoom Multiple Images Per Product",

    'summary': """
        Upload several high quality images for your products and let customers enlarge and zoom them for clarity. Choose from numerous zoom options per product  """,

    'description': """
        This Module will make it possible to add unlimited number of images for the website product. With an option to publish/unpublish, zoom in or out, magnify in different styles configurable per product.
    """,
    'images': ['static/description/main1.png'],
    'author': "Optima ICT Services LTD",
    'website': "http://optima.co.ke",
    'price': 49,
    'currency': 'EUR',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
	'views/product_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
