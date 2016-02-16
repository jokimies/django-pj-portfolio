'use strict';

describe('Positions service', function () {
    var $httpBackend, Positions, $rootScope;

    beforeEach(module('portfolio'));

    beforeEach(inject(function($controller, _$rootScope_, 
                               _$httpBackend_, _Positions_) {
        $httpBackend = _$httpBackend_;
        Positions = _Positions_;
        $rootScope = _$rootScope_;
        jasmine.getJSONFixtures().fixturesPath='base/portfolio/static/tests/mock';
        
        $httpBackend.whenGET('/portfolio/api/v1/positions/1/')
            .respond(getJSONFixture('positions_detail.json'));
    }));

    it('should have some results', function() {
        var result;
        Positions.all('1').then(function (data) {
            result = data.data;
            expect(result['Whitestone REIT'].price).toEqual(10.75);
        }, function(data) {
            console.log("Error", data);
        });

        $httpBackend.flush();
    });

    it('should calculate market value correctly', function() {

        var positions;
        var mktval;

        Positions.all('1').then(function (data) {
            positions = data.data;
        }, function(data) {
            console.log("Error", data);
        });

        $httpBackend.flush();

        mktval = Positions.market_value(positions);
        expect(mktval).toBeCloseTo(18884.6, 2);

    });
});
