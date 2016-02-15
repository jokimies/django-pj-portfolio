(function () {
    'use strict';

    angular
        .module('portfolio.config')
        .config(config);

    config.$inject = ['$locationProvider'];

    /**
     * @name config
     * @desc Enable HTML5 mode
     */

    function config($locationProvider) {
        $locationProvider.html5Mode(true);
    }
})();
