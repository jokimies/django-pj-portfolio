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
            yahoo_quote: yahoo_quote,
            google_local_quote: google_local_quote
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
        
        function yahoo_quote(security) {
            var query = 'select * from yahoo.finance.quotes where symbol = "' + 
                    security + '"';
            var format = '&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=JSON_CALLBACK';
            var url = 'https://query.yahooapis.com/v1/public/yql?q=' +
                    encodeURIComponent(query) + '%0A%09%09' + format;
            return $http.jsonp(url);
        }

        /**
         * Google quote using local backend as proxy to prevent
         * No ‘Access-Control-Allow-Origin’ header is present on the
         * requested resource. Origin ‘xxx’ is therefore not allowed
         * access. Python's requests lib doesn't care if the header is
         * there or not, browser does.
         */
        function google_local_quote(security) {
            return $http.get('/portfolio/api/v1/' + security + '/quote/');
        }
    }
})();
