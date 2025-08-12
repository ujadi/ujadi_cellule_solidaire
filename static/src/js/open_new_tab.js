odoo.define('cellule_solidaire_ujadi.open_new_tab_button', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;

    var OpenNewTabButton = Widget.extend({
        events: {
            'click .open-new-tab-btn': '_onClickOpenNewTab',
        },

        start: function () {
            this.$el.html(QWeb.render('cellule_solidaire_ujadi.OpenNewTabButtonTemplate'));
            return this._super.apply(this, arguments);
        },

        _onClickOpenNewTab: function () {
            var self = this;
            this._rpc({
                model: 'livre.syntetique.custom',
                method: 'create',
                args: [{}],
            }).then(function (record_id) {
                var url = '/web#id=' + record_id + '&model=livre.syntetique.custom&view_type=form';
                window.open(url, '_blank', 'width=1024,height=768');
            });
        },
    });

    core.action_registry.add('open_new_tab_button', OpenNewTabButton);

    return OpenNewTabButton;
});
