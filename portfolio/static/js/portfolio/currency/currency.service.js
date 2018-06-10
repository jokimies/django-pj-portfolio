(function () {
    'use strict';

    angular
        .module('portfolio.currency')
        .factory('Currencies', Currencies);

    Currencies.$input = ['$http', '$sce'];

    /**
     * @
     * @desc
     */

    function Currencies($http, $sce) {
        var Currencies = {
            all: all
        };
        
        return Currencies;

        /**
         * @
         * @name all
         */
        function all() {
            var url = '/portfolio/api/v1/exchange/';
            $sce.trustAsResourceUrl(url);
            return $http.get(url);
        }
    }
})();
