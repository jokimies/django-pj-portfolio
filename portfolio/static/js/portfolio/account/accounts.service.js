(function () {
    'use strict';

    angular
        .module('portfolio.account.service')
        .factory('Accounts', Accounts);

    Accounts.$inject = ['$http'];
    
    /**
     * @
     * @desc
     */

    function Accounts($http) {
        var Accounts = {
            all: all,
        };

        return Accounts;

        /**
         * @name all
         *
         */

        function all() {
            return $http.get('/portfolio/api/v1/accounts/');
        }
    }
})();

