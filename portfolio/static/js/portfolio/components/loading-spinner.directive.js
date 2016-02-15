(function () {
    'use strict';

    angular.module('loadingSpinner')
    .directive('usSpinner', usSpinner);

    usSpinner.$inject = ['$http', '$rootScope'];

    function usSpinner($http, $rootScope) {
        return {
          link: function (scope, elm, attrs)
            {
                $rootScope.spinnerActive = false;
                scope.isLoading = function () {
                    return $http.pendingRequests.length > 0;
                };

                scope.$watch(scope.isLoading, function (loading)
                {
                    $rootScope.spinnerActive = loading;
                    if(loading){
                        elm.removeClass('ng-hide');
                    }else{
                        elm.addClass('ng-hide');
                    }
                });
            }
        };  
    }

})();
