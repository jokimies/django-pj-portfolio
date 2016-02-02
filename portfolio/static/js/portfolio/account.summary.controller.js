/**
 * PortfolioAccountSummaryController
 * @namespace portfolio.account.summary.controller
 */

(function () {
    
    'use strict';

    angular
        .module('portfolio.account.summary')
        .controller('AccountSummaryController', 
                    AccountSummaryController);

    AccountSummaryController.$inject = [ '$timeout', '$q', 'Positions', 
                                         'Securities'];

    function AccountSummaryController($timeout, $q, Positions, Securities) {
        var vm = this;

        var promises = {
            positions: Positions.all(),
            securities: Securities.all(),
        }

        /* 
           for now, Securities.all() returns an array, dictionary needed to
           be able to easily map ticker to name
        */
        vm.securities_d = {};

        activate();

        /**
         * @name activate
         * @desc 
         * @memberOf portfolio.accountsummary.controller.AccountSummaryController
         */
        function activate() {

            $q.all(promises).then(promisesSuccessFn, promisesErrorFn);

            console.log($q);
            /**
             * @name positionsSuccessFn
             * @desc
             */
            function promisesSuccessFn(data, status, headers, config) {
                vm.positions = data.positions.data;
                vm.securities = data.securities.data;
                console.log("promisesSuccessFn");
                getLivePrices();

            }

            function promisesErrorFn(data, status, headers, config) {
                console.log('promisesErrorFn')
                console.log(data);
            }
        }


        function getLivePrices() {
                
            var i, delay;
            var minTime = 1000; // 1 sec
            var maxTime = 4000; // 4 secs
            var refreshRate = 10; // minutes
            var ticker;

            for(i=0; i<vm.securities.length; i++) {
                ticker = vm.securities[i].ticker;
                vm.securities_d[ticker] = vm.securities[i].name;
                console.log(ticker);
                delay = Math.floor(Math.random()*(maxTime-minTime+1)+minTime);
                console.log('Delay on ', delay);

                /* call getQuoteForSecurity with 'ticker' argument */
                $timeout(getQuoteForSecurity.bind(null, ticker),
                         delay);
            }

            $timeout(function () {
                getLivePrices();
            }, refreshRate*60*1000);
            
            function getQuoteForSecurity(ticker) {

                Positions.google_quote(ticker)
                    .then(positionsLiveSuccessFn, positionsLiveErrorFn);
            }
                
            function positionsLiveSuccessFn(data, status, headers, config) {

                var securityName;

                if (typeof vm.positions === 'undefined') {
                    /* It should be impossible to get here with
                       vm.positions undefined, but just in case, do nothing  */
                    ;
                }
                else {
                    /* t represents ticker */
                    if ( typeof data[0]['t'] !== 'undefined' ) {

                        securityName = vm.securities_d[data[0]['t']];

                        /* 
                           vm.positions has securities whise count is
                           greater than zero. However, Securities.all() 
                           service returns all securities in DB. Hence
                           it is possible that vm.positions[securityName]
                           is not defined
                        */
                        if ( typeof vm.positions[securityName] !== 'undefined' ) {
                                                    /* l is latest value */

                            vm.positions[securityName]['price'] = data[0]['l'];
                            vm.positions[securityName]['change'] = data[0]['c'];
                            vm.positions[securityName]['change_percentage'] = data[0]['cp'];
                        }
                    }
                }
            }

            function positionsLiveErrorFn(data) {
                if (data.statusText === 'error') {
                    console.log('LiveError: Ketuiksi meni', data);
                }
                else {
                    console.log('LiveError', data)
                }
            }

        }
    }
})();
