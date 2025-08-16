from odoo import models, fields, api


class CelluleSetDraftWizard(models.TransientModel):
    _name = 'cellule.set.draft.wizard'
    _description = 'Wizard to set Cellule Solidaire to draft state'


    raison = fields.Text(string='Raison', required=True, help='Raison pour laquelle la cellule est remise en état draft.')

    def action_confirm(self):
        """Set the Cellule Solidaire to draft state."""
        cellule = self.env['cellule.solidaire'].browse(self._context.get('active_id'))
        cellule.write({
            'state': 'draft',
            'remise_raison': self.raison,
        })
        cellule.message_post(
            body=f"La cellule a été remise en état draft pour la raison suivante : {self.raison}",
        )
        