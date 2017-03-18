# -*- coding: utf-8 -*-
# Copyright 2017 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, exceptions


class InterventionStage(models.Model):
    _name = 'intervention.stage'
    _description = 'Stage'
    _order = 'sequence, id'

    def _get_default_team_ids(self):
        team_id = self.env.context.get('default_team_id')
        if team_id:
            return [(4, team_id, 0)]

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(String='Sequence', default=10)
    is_close = fields.Boolean(
        string='Closing Kanban Stage',
        help='Requests in this stage are considered as done.')
    fold = fields.Boolean(
        string='Folded', help='Folded in kanban view')
    team_ids = fields.Many2many(
        comodel_name='intervention.team', string='Team',
        default=_get_default_team_ids,
        help='Specific team that uses this stage. Other teams will not be able to see or use this stage.')
