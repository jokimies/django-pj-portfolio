'use strict';

describe('AccountSummaryController', function() {

    var ctrl;
    var $scope;

    beforeEach(module('portfolio'));

    beforeEach(inject(function($controller) {

        ctrl = $controller('AccountSummaryController');

    }));


    it('should have controller defined', function() {
        expect(ctrl).toBeDefined();
    }); 
});
