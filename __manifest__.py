# -*- coding: utf-8 -*-
{
    'name': "Kedai Pondok Family",

    'summary': """
        Program untuk mengelola ketersediaan barang dan inventory Kedai Pondok Family""",

    'description': """
        Long description of module's purpose
    """,

    'author': "AlFarkhan",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/pf_menu.xml',
        'views/pf_viewbahandasar.xml',
        # 'views/pf_viewrestokbahan.xml',
        'views/pf_viewlistmenu.xml',
        'views/pf_vieworderlist.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
