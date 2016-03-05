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

    AccountSummaryController.$inject = [ '$timeout', '$q', '$location',
                                         'Positions',
                                         'Securities', 'Accounts',
                                         'Currencies'];

    function AccountSummaryController($timeout, $q, $location, Positions,
                                      Securities, Accounts, Currencies) {
        var vm = this;

        vm.sortReverse = false;
        vm.sortColumn = '$key';

        /* Get the account id from URL */
        var accountID = $location.path().split("/")[3];

        var promises = {
            positions: Positions.all(accountID),
            securities: Securities.all(),
            accounts: Accounts.all(),
            currencies: Currencies.all(),
        }

        /* 
           for now, Securities.all() returns an array, dictionary needed to
           be able to easily map ticker to name
        */
        vm.securities_d = {};

        vm.total_mktval = 0;

        activate();

        /**
         * @name activate
         * @desc 
         * @memberOf portfolio.accountsummary.controller.AccountSummaryController
         */
        function activate() {

            $q.all(promises).then(promisesSuccessFn, promisesErrorFn);

            /**
             * @name positionsSuccessFn
             * @desc
             */
            function promisesSuccessFn(data, status, headers, config) {
                vm.positions = data.positions.data;
                vm.securities = data.securities.data;
                vm.accounts = data.accounts.data;
                vm.currencies = data.currencies.data
                getLivePrices();

            }

            function promisesErrorFn(data, status, headers, config) {
                console.log('promisesErrorFn', data);
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
                delay = Math.floor(Math.random()*(maxTime-minTime+1)+minTime);

                /* call getQuoteForSecurity with 'ticker' argument */
                $timeout(getQuoteForSecurity, delay, true, ticker);

            }

            vm.liveTimer = $timeout(function () {
                getLivePrices();
            }, refreshRate*60*1000);
            
            function getQuoteForSecurity(ticker) {

                Positions.google_quote(ticker)
                    .then(positionsLiveSuccessFn, positionsLiveErrorFn);
            }
                
            function positionsLiveSuccessFn(data, status, headers, config) {

                var securityName;
                var securityCurrency;
                var ltDateSecs; /* latest transactrion date in seconds */

                if (typeof vm.positions === 'undefined') {
                    /* It should be impossible to get here with
                       vm.positions undefined, but just in case, do nothing  */
                    ;
                }
                else {
                    /* t represents ticker */
                    if ( typeof data[0]['t'] !== 'undefined' ) {

                        securityName = vm.securities_d[data[0]['t']];
                        securityCurrency = getCurrency(data[0]['l_cur']);
                        fx.base = vm.currencies['base'];
                        fx.rates = vm.currencies.rates;

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
                            /* parse return milliseconds, second wanted */
                            ltDateSecs = Date.parse(data[0]['lt_dts']) / 1000;
                            vm.positions[securityName]['latest_date'] =
                                moment.unix(ltDateSecs).format('YYYY-MM-DD');
                            /* convert currency unsed in security price
                               to base currency and used the converted
                               value as market value for the security in
                               questinon 
                            */

                            vm.positions[securityName]['mktval'] = 
                                fx(vm.positions[securityName]['price'] * 
                                vm.positions[securityName]['shares']) 
                                .from(securityCurrency).to(fx.base);
                            vm.total_mktval = 0;
                            for (var position in vm.positions) {
                                if (vm.positions.hasOwnProperty(position)) {
                                    vm.total_mktval += vm.positions[position]['mktval'];
                                }
                            }
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
 
            function getCurrency(l_cur) {
                /* 
                 * l_cur represents lates value with currency
                 */
                if (l_cur.indexOf("\u20ac") !== -1 ) {
                    return 'EUR';
                } else {
                    return 'USD';
                }
            }
        }
    }
})();
