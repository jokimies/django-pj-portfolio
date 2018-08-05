(function () {
    'use strict';

    angular
        .module('portfolio')
        .config(config);

    config.$inject = [ '$routeProvider' ];

    function config($routeProvider) {

        $routeProvider
            .when('/securities', {
                controller: 'SecuritiesIndexController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/layout/securities.html'
            })
            .otherwise('/');
        }
})();
