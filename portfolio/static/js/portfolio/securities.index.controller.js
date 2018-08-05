/**
 * SecuritiesIndexController
 *
 */
(function () {
    'use strict';

    angular
	.module('portfolio.securities')
	.controller('SecuritiesIndexController', SecuritiesIndexController);

    SecuritiesIndexController.$inject = ['$scope', 'Securities', '$location'];

    /**
     * SecuritiesIndexController
     */
    function SecuritiesIndexController($scope, Securities, $location ) {
	var vm = this;
	vm.securities = [];
        console.log('BUU', $location.path(), $location.absUrl());
	activate();

	/**
	 * activate
	 *
	 */
	function activate() {
	    Securities.all().then(securitiesSuccessFn, securitiesErrorFn);

	    /**
	     * securitiesSuccessFn
	     *
	     */ 
	    function securitiesSuccessFn(data, status, headers, config){
		vm.securities = data.data;
	    }

	    /**
	     * securitiesErrorFn
	     */
	    function securitiesErrorFn(data, status, headers, config) {
		console.log(data.error);
	    }
	}
    }
})();

	    
