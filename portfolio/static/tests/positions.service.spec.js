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
        Positions.all().then(function (data) {
            result = data.data;
            expect(result['Metso'].price).toEqual(18);
        }, function(data) {
            console.log("Error", data);
        });

        $httpBackend.flush();
    });

});
