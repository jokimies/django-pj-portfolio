(function () {
    'use strict';

    describe('Positions service', function () {
        var $httpBackend, Positions, $rootScope;
        var googleQuoteTicker = 'WSR';
        var positionJSON = 'positions_detail.json';

        beforeEach(module('portfolio'));

        beforeEach(inject(function($controller, _$rootScope_,
                                   _$httpBackend_, _Positions_) {

            /* Fixtures get cached. In case other tests are changing the
               cache, remove  it.. and reload later
            */
            var fixtures = loadJSONFixtures(positionJSON);
            delete fixtures[positionJSON];

            $httpBackend = _$httpBackend_;
            Positions = _Positions_;
            $rootScope = _$rootScope_;

            jasmine.getJSONFixtures().fixturesPath='base/portfolio/static/tests/mock';
        }));

        it('should get quote from Google', function() {
            var response;

            $httpBackend.expectJSONP('http://finance.google.com/finance/info?callback=JSON_CALLBACK&client=ig&q=' + googleQuoteTicker)
                .respond(getJSONFixture('google_quote.json'));

            Positions.google_quote(googleQuoteTicker).then(function(data){
                response = data;
            }, function(data) {
                console.log('google_quote error ', data);
            });
            $httpBackend.flush();
            expect(response[0]['t']).toEqual(googleQuoteTicker);
        });

        it('should have some results', function() {
            var result;

            $httpBackend.whenGET('/portfolio/api/v1/positions/1/')
                .respond(getJSONFixture('positions_detail.json'));

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

            $httpBackend.whenGET('/portfolio/api/v1/positions/1/')
                .respond(getJSONFixture(positionJSON));

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
})();
