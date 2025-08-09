from odoo import models, fields, api
class DeleteMembreWizard(models.TransientModel):
    _name = 'delete.membre.cs.wizard'
    _description = 'Wizard de confirmation de suppression de membre'

    membre_id = fields.Many2one('membre.cs', string="Membre à supprimer", required=True)

    def confirm_delete(self):
        self.ensure_one()
        self.membre_id.unlink()
        return {'type': 'ir.actions.act_window_close'}
