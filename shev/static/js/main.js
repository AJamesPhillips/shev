$(document).ready(function(){
    // Routing
    var Router = Backbone.Router.extend({
        routes: {
            'roster/overview/': 'overview',
            'roster/day/:year/:month/:day/': 'day',
            'roster/person/:pkid/': 'person',
        },
        overview: function () {
            window.overview_view()
        },
        day: function (year, month, day) {
            window.day_view()
        },
        person: function (pkid) {
            window.person_view()
        },
    });
    var router = new Router();
    // we're not using backbone the way it was intended but it works
    Backbone.history.loadUrl(window.location.pathname)
});