(function() {
    'use strict';

    angular
        .module('portfolio')
        .constant('portfolioConfig', {
            APIMinWaitTime: 5000, // 5 secs
            APIMaxWaitTime: 10000 // 10 secs
        });
}());
