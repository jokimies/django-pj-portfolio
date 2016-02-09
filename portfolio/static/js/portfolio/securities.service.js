/**
 * Securities
 *
 */
(function () {
    'use strict';
    
    angular
	.module('portfolio.securities')
	.factory('Securities', Securities);

    Securities.$inject = ['$http'];
    /**
     * Securities
     * @returns {Factory}
     */
    function Securities($http) {
	var Securities = {
	    all: all,
	    get: get,
	    add: add
	};
	return Securities;

	/**
	 * @name all
	 * @desc Get all Securities
	 * @returns {Promise}
	 */
	function all() {
	    return $http.get('/portfolio/api/v1/securities/');
	}

	function get() {
	    return $http.get('/api/v1/securities/');
	}
	
	function add(name, ticker) {
	    return $http.post('/portfolio/api/v1/securities/', {
		name: name,
		ticker: ticker
	    }).then(addSuccessFn, addErrorFn);

	    function addSuccessFn(data, status, headers, config) {
		console.log("Added");
	    }
	    function addErrorFn(data, status, headers, config) {
		console.error('Epic failure!');
	    }
	}
    }
})();
