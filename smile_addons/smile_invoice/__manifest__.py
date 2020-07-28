# -*- coding: utf-8 -*-
{
    'name': "Smile Invoice",
    'description': """
        This project was created to manage invoicing
    """,

    'author': "Invoice",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    "license": 'LGPL-3',
    'version': '0.1',

    "installable": True,
    "active": True,

    'depends': ['base', 'sale'],
    'data': [
        # Security
        'security/ir.model.access.csv',
    ],


}
