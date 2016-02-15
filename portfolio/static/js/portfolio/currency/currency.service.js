(function () {
    'use strict';

    angular
        .module('portfolio.currency')
        .factory('Currencies', Currencies);

    Currencies.$input = ['$http'];

    /**
     * @
     * @desc
     */

    function Currencies($http) {
        var Currencies = {
            all: all
        };
        
        return Currencies;

        /**
         * @
         * @name all
         */
        function all() {
            return $http.jsonp('http://api.fixer.io/latest?callback=JSON_CALLBACK');
        }
    }
})();
