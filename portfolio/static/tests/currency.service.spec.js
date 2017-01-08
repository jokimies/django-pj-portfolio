'use strict';

describe('Currency service', function() {
    var $httpBackend, Securities, $rootScope, Currencies;

    beforeEach(module('portfolio'));

    beforeEach(inject(function($controller, _$rootScope_, _$httpBackend_,
                      _Currencies_) {
        $httpBackend = _$httpBackend_;
        Currencies = _Currencies_;
        $rootScope = _$rootScope_;
        jasmine.getJSONFixtures().fixturesPath='base/portfolio/static/tests/mock';
        $httpBackend
            .whenGET('https://api.fixer.io/latest')
            .respond(getJSONFixture('currencies.json'));
    }));

    it('shoud return exchange rates', function() {
        var result;

        Currencies.all().then(function(data) {
            result = data.data;
        }, function(data) {
            console.log('Currencies.all() error: ', data);
        });
       
        $httpBackend.flush();

        expect(result['rates']['USD']).toEqual(1.0540);
        
    });
});
