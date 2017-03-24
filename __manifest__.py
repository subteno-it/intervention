# -*- coding: utf-8 -*-
# Copyright 2017 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'intervention',
    'version': '10.0.1.0.0',
    'category': 'Custom',
    'summary': 'Managing Intervention Requests',
    'author': 'Sebastien LANGE',
    'website': 'http://www.syleam.fr',
    'depends': [
        'base',
        'mail',
        'report',
    ],
    'description': """
Intervention - Intervention Management App
==========================================

Features:

    - TODO

    """,
    'data': [
        'security/intervention_security.xml',
        'security/ir.model.access.csv',

        'data/ir_sequence.xml',
        'data/intervention_team.xml',
        'data/intervention_stage.xml',

        'report/actions.xml',
        'report/assets.xml',
        'report/intervention_voucher_document.xml',
        'report/intervention_report_document.xml',

        'views/intervention_request.xml',
        'views/intervention_tag.xml',
        'views/intervention_team.xml',
        'views/intervention_stage.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': True,
}
