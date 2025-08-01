{
    'name': 'UJADI ONGD - Cellule Solidaire',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Module for managing Ujadi Cellule Solidaire operations',
    'description': 'This module is designed to manage the operations of Ujadi Cellule Solidaire, including member management, event organization, and donation tracking.',
    'author': 'Annette Bwemere',
    'website': 'https://www.ujadiongd.com',
    'depends': [
        'base_setup',
        'base', 
        'mail', 
        'web'
    ],
    'data': [
       'security/ir.model.access.csv',
       'views/cellule_solidaire_views.xml',
       'views/membre_cs_views.xml',
       'views/responsable_cs_views.xml',
       'views/cellule_solidaire_menus.xml',
       'data/cellule_solidaire_data.xml',
       'data/responsable_cs_data.xml',
       'data/membre_cs_data.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}