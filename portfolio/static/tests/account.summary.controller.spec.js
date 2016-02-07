'use strict';

describe('AccountSummaryController', function() {

    var ctrl;
    var $q, testSecurities, testPositions;
    var $scope;

    beforeEach(module('portfolio'));

    beforeEach(inject(function($controller, _$q_, _$rootScope_, _Positions_, _Securities_) {
        testSecurities = _Securities_;
        testPositions = _Positions_;
        $scope = _$rootScope_.$new();
        $q = _$q_;

        ctrl = $controller('AccountSummaryController', 
                           { 
                               Securities: testSecurities,
                               Positions: testPositions,
                               $q: $q,
                           });
        spyOn(testPositions, 'all'); 
    }));

    afterEach(function(){
        //$scope.$apply();
    });

    it('should have controller defined', function() {
        expect(ctrl).toBeDefined();
    }); 
});
