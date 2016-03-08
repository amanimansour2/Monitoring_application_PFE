(function(){
var app= angular.module('monitoringgeneral', []);
app.controller('monitoringgeneralcontroller', ['$scope','$http', function($scope,$http) {
  
     $scope.volfile = function () {
          $http({
                  method : "GET",
                  url : "/monitoring_app/statusgeneral/",
                  }).then(function(response) {

				          v=response.data.volfile
						  d=response.data.delay
                          return v+" "+d;
                  });}   
}]);
})();


