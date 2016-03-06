(function () {
    'use strict';
    
    angular
        .module('portfolio.account.summary')
        .directive('highlight', Highlight);

    Highlight.$inject = ['$animate', '$timeout'];

    function Highlight($animate, $timeout) {

        return function(scope, element, attributes) {
            scope.$watch(attributes.highlight, function(newValue,oldValue) {
                if (newValue != oldValue) {
                    var newClass = newValue > oldValue ? 'highlight-green'
                        : 'highlight-red';
                    element.addClass(newClass);
                    /* remove new class after a while */
                    $timeout(function () {
                        element.removeClass(newClass);
                    },300);
                }
            });
        }
    }
})();
