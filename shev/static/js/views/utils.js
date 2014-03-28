window.setupDateTables = function (cssSelector, options) {
    options = options || {};
    options = _.extend({
        aoColumnDefs: [
            { bSortable: true, aTargets: [ '_all' ] }
        ],
        // This isn't needed as we use jquery to hide the option
        // aLengthMenu: [
        //     [-1],
        //     ["All"],
        // ],
        iDisplayLength: -1,
    }, options)
    $(cssSelector).dataTable(options);
    $('.dataTables_length').hide();
    $('.dataTables_info').hide();
    $('.dataTables_paginate').hide();
};