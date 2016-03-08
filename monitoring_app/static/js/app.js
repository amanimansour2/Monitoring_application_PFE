
(function(){
var app= angular.module('monitoring', []);
app.controller('monitoringcontroller', ['$scope','$http', function($scope,$http) {
    
    $scope.status = function () {
          return "ffffff";}   
		  
	$scope.firewall='status firewall';
    $scope.getfirewallstatus = function() {
        $http({
                method : "GET",
                url : "/monitoring_app/statusfirewall/",
                 }).then(function(response) {
                           $scope.firewall= response.data.firewall;
                  });}

     $scope.route='default route';
     $scope.getroute = function() {
          $http({
                  method : "GET",
                  url : "/monitoring_app/route/",
                  }).then(function(response) {

                          $scope.route= response.data.route;
                  });}

     $scope.cpu='cpu usage';
     $scope.getcpu = function() {
          $http({
                  method : "GET",
                  url : "/monitoring_app/cpu/",
                  }).then(function(response) {

                          $scope.cpu= response.data.cpu;
                  });}

    
     $scope.disk='usage disk';
     $scope.getdisk = function () {
          $http({
                  method : "GET",
                  url : "/monitoring_app/disk/",
                  }).then(function(response) {

                          $scope.disk= response.data.disk;
                  });}

     $scope.volfile='voluminous file';
     $scope.getvolfile = function () {
          $http({
                  method : "GET",
                  url : "/monitoring_app/voluminousfile/",
                  }).then(function(response) {

                          $scope.volfile= response.data.volfile;
                  });}

    $scope.servicedhcp='status service dhcp';
    $scope.servicedns='status service dns';
    $scope.servicentp='status service ntp';
    $scope.servicefree='status service Freeswitch'
    $scope.getservicesstatus = function() {
           $http({
                    method : "GET",
                    url : "/monitoring_app/services/", 
                   }).then(function(response) {
                             $scope.servicedhcp= response.data.dhcpstatus;
                             $scope.servicedns= response.data.dnsstatus;
                             $scope.servicentp= response.data.ntpstatus;
                              $scope.servicefree= response.data.freestatus;
                     });}

   
    $scope.delay = 'status';
    $scope.getdelay = function() {
            $http({
                      method : "GET",
                      url : "/monitoring_app/delay/",
                       }).then(function(response) {
                              $scope.delay= response.data.delay;
                        });}
    
    $scope.input = "enter the process name";
    $scope.name = 'pid number';
    $scope.getpid = function() {
              $http({
                      method : "GET",
                      url : "/monitoring_app/getpid/",
                      params:{"pidname" :$scope.input},
                       }).then(function (response) {
                                $scope.name = response.data.pidname;
                        });}
}]);
})();


