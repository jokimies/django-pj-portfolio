'use strict';

describe('Securities service', function () {
    var $httpBackend, Securities, $rootScope;

    beforeEach(module('portfolio'));

    beforeEach(inject(function($controller, _$rootScope_, 
                               _$httpBackend_, _Securities_) {
        $httpBackend = _$httpBackend_;
        Securities = _Securities_;
        $rootScope = _$rootScope_;
        jasmine.getJSONFixtures().fixturesPath='base/portfolio/static/tests/mock';
        
        $httpBackend.whenGET('/portfolio/api/v1/securities/')
            .respond(getJSONFixture('securities.json'));
    }));
         
    it('should have some results', function() {
        var result;
        Securities.all().then(function (data, status) {
            result = data.data;
            expect(result[0].name).toEqual('Nordea Bank');
        }, function(data) {
            console.log("Error", data);
        });

        $httpBackend.flush();
    });
});
       
