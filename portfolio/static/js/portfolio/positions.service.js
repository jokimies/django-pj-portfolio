/**
 * Positions
 * @namespaces portfolio.positions.services
 */

(function () {
    'use strict';

    angular
        .module('portfolio.positions.services')
        .factory('Positions', Positions);

    Positions.$inject = ['$http', '$resource'];

    /**
     * @
     * @desc
     */
    function Positions($http, $resource) {
        var Positions = {
            all: all,
            google_quote: google_quote,
            market_value: market_value,
        };
        
        return Positions;

        /**
         * @name all
         *
         */
        function all(accountID) {
            return $http.get('/portfolio/api/v1/positions/' + accountID + '/');
        }

        function google_quote(security) {
            var url = 'http://finance.google.com/finance/info?q=' + security;
            console.log('url', url);
            var quote = $resource('http://finance.google.com/finance/info', 
                                     {client:'ig', callback:'JSON_CALLBACK'},
                                     {get: {method:'JSONP', params:{q:security}, 
                                            isArray: true}});
            return quote.get().$promise
        }

        function market_value(positions) {

            var position;
            var total = 0;

            for (position in positions) {
                if (positions.hasOwnProperty(position)) {
                    total += positions[position]['mktval'];
                }
            }
            return total;
        }
    }
})();
