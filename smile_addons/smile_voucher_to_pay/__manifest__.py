# -*- coding: utf-8 -*-
{
    'name': "Smile Voucher to pay",
    'description': """
        This project was created to manage orders and purchase
    """,

    'author': "Smile",
    'website': "http://www.smile.com",

    'category': 'Uncategorized',
    "license": 'LGPL-3',
    'version': '0.1',

    "installable": True,
    "active": True,

    'depends': ['base', 'purchase', 'account'],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # views
        'views/invoice_view.xml',
        'views/user_view.xml',
    ],
}
