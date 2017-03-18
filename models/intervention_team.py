# -*- coding: utf-8 -*-
# Copyright 2017 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, exceptions


class InterventionTeam(models.Model):
    _name = 'intervention.team'
    _description = 'Intervention Team'
    _order = 'sequence,name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string='Intervention Team', required=True, translate=True)
    description = fields.Text(string='About Team', translate=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get('intervention.team'))
    sequence = fields.Integer(default=10)
    color = fields.Integer(string='Color Index')
    stage_ids = fields.Many2many(
        comodel_name='intervention.stage', string='Stages',
        default=[(0, 0, {'name': 'New', 'sequence': 0})],
        help="Stages the team will use. This team's requests will only be able to be in these stages.")
    member_ids = fields.Many2many(
        comodel_name='res.users', string='Team Members',
        domain=lambda self: [('groups_id', 'in', self.env.ref('base.group_intervention_user').id)])
    request_ids = fields.One2many(
        comodel_name='intervention.request', inverse_name='team_id', string='Requests')

