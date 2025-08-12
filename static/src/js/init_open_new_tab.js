odoo.define('cellule_solidaire_ujadi.init_open_new_tab_button', function (require) {
    "use strict";

    var OpenNewTabButton = require('cellule_solidaire_ujadi.open_new_tab_button');

    $(document).ready(function () {
        var $container = $('#open_new_tab_button_container');
        if ($container.length) {
            new OpenNewTabButton(null, {}).appendTo($container);
        }
    });
});
