window.day_view = function () {
    // define some custom datatable sorters
    jQuery.fn.dataTableExt.oSort['btp-pre']  = function(val) {
        var sortVal = parseInt(val, 10);
        if (_.isNumber(sortVal) && (! _.isNaN(sortVal))) {
            'do nothing';
        } else if (val === 'Supernumerary') {
            sortVal = 0;
        } else {
            sortVal = 1;
        }
        console.log(val, sortVal);
        return sortVal;
    };

    jQuery.fn.dataTableExt.oSort['btp-asc']  = function(x,y) {
        return ((x < y) ? -1 : ((x > y) ?  1 : 0));
    };

    jQuery.fn.dataTableExt.oSort['btp-desc'] = function(x,y) {
        return ((x < y) ?  1 : ((x > y) ? -1 : 0));
    };

    $('.shifts').dataTable({
        aaSorting: [[ 0, "desc" ]],
        aoColumnDefs: [
            { bSortable: true, aTargets: [ 0 ], sType: "btp",  },
            { bSortable: true, aTargets: [ '_all' ] }
        ],
        // This isn't needed as we use jquery to hide the option
        // aLengthMenu: [
        //     [-1],
        //     ["All"],
        // ],
        iDisplayLength: -1,
    });
    $('.dataTables_length').hide();
    $('.dataTables_info').hide();
    $('.dataTables_paginate').hide();

}