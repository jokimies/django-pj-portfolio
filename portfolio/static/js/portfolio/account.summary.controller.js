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
                vm.currencies = data.currencies.data;
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
            
            function getQuoteForSecurity(ticker, provider) {
                /* Stupid workaround for lack of default parameters ... */
                provider  = (typeof provider !== 'undefined') ?  
                        provider : 'yahoo';
                /* Two possible providers for quote, Google and Yahoo */
                switch(provider) {
                    case 'yahoo':
                    Positions.yahoo_quote(ticker)
                        .then(positionsLiveSuccessYahooFn, 
                              positionsLiveErrorYahooFn);
                    break;
                    case 'google':
                    Positions.google_quote(ticker)
                        .then(positionsLiveSuccessFn, positionsLiveErrorFn);
                    break;
                }
            }
                
            function positionsLiveSuccessYahooFn(data, status, headers, config) {

                var result;
                var ticker;
                var currency;
                var price;
                var changePercentage;
                var change;
                var lastTrade;
                
                /* Yahoo returns 'null' as value for every field if we're
                 * asking for quote for unknown ticker 
                 * ... or it might not return 'results' at all
                 * ... or eg. Change can be null if there're no transactions
                 * for today
                 */ 

                if ( data.data.query.results !== null ) {
                    result = data.data.query.results.quote;
                    ticker = result.symbol;
                    currency = result.Currency;
                    price = result.LastTradePriceOnly;
                    changePercentage = result.ChangeinPercent;
                    change = result.Change;
                    lastTrade = result.LastTradeDate;
                }
                if (  change === null || result === undefined ) {
                    return;
                }
             
                /* Strip off % character */
                changePercentage = changePercentage.slice(0, -1);
                
                populateSecurityData(ticker, currency, price,
                                     changePercentage, change,
                                     lastTrade);
            }

            function positionsLiveSuccessFn(data, status, headers, config) {

                var result = data[0];
                var ticker = result['t'];
                var currency = result['l_cur'];
                var price = result['lt_dts'];
                var changePercentage = result['cp'];
                var change = result['c'];
                var lastTrade = result['lt_dts'];

                populateSecurityData(ticker, currency, price,
                                     changePercentage, change,
                                     lastTrade);
            }


            function populateSecurityData(ticker, currency, price, 
                                          changePercentage,
                                          change, lastTrade) {

                var securityName;
                var securityCurrency;
                var ltDateSecs;

                if (typeof vm.positions === 'undefined') {
                    /* It should be impossible to get here with
                       vm.positions undefined, but just in case, do nothing  */
                    ;
                }
                else {
                    /* If ticker is not found, Yahoo returns null */
                    if ( typeof ticker !== 'undefined' ||  ticker !== null) {
                        securityName = vm.securities_d[ticker];
                        securityCurrency = getCurrency(currency);
                        fx.base = vm.currencies['base'];
                        fx.rates = vm.currencies.rates;
                        
                        /* 
                           vm.positions has securities whose count is
                           greater than zero. However, Securities.all() 
                           service returns all securities in DB. Hence
                           it is possible that vm.positions[securityName]
                           is not defined
                        */
                        if ( typeof vm.positions[securityName] !== 'undefined' ) {
                            /* l is latest value */
                            vm.positions[securityName]['price'] = price;
                            vm.positions[securityName]['change'] = change;
                            vm.positions[securityName]['change_percentage'] = changePercentage;
                            /* parse return milliseconds, second wanted */
                            ltDateSecs = Date.parse(lastTrade) / 1000;
                            vm.positions[securityName]['latest_date'] =
                                moment.unix(ltDateSecs).format('YYYY-MM-DD');
                            /* convert currency uned in security price
                               to base currency and use the converted
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
            function positionsLiveErrorYahooFn(data, status, headers, config) {
                console.log(data);
                console.log("Failed fetching data from Yahoo");
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
