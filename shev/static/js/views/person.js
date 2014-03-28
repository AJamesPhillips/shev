window.person_view = function() {
    var options = {
        aaSorting: [[ 1, "desc" ]],
        aoColumnDefs: [
            { bSortable: true, aTargets: [ '_all' ] }
        ],
    };
    window.setupDateTables('.shifts', options);
};