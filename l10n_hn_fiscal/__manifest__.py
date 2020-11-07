# -*- coding: utf-8 -*-
{
    'name': 'Facturacion SAR',
    'version': '11.0.1.2',
    'category': 'Account',
    'author': 'IT Solutions',
    'depends': [
                'account',
                'base',
                'sale_management',
                ],
    'data':[
        'data/report_paperformat_data.xml',
        'data/account.tax.group.csv',
        'data/account.tax.csv',
        'report/report_general.xml',
        'wizard/report_general.xml',
        'report/report_general_purchase.xml',
        'wizard/report_general_purchase.xml',
        'report/report_invoice.xml',
        'views/ir_sequence.xml',
        'views/account_invoice.xml',
        'views/res_group.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
}   
