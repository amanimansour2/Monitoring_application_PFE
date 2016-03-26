(function(){
var app= angular.module('monitoring', []);
app.controller('monitoringcontroller', ['$scope','$http', function($scope,$http) {
    $scope.status='click sur Get ';
	$scope.statusge= function($id) {
        $http({
		method : "GET",
		url : "/monitoring_app/statusgeneral/",
	    params:{"id" : $id},
		}).then(function(response) {
			$scope.status=response.data.status;
			
		});			}
	$scope.getmachine2 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/regphone/",
						 }).then(function(response) {
								   $scope.phone= response.data.phone;
			});  }
	$scope.stat='No';
    $scope.getmachine3 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/freeswitchcommunication/",
						 }).then(function(response) {
								   $scope.stat= response.data.stat;

			});  }
	 $scope.confnumber='1000';
	 $scope.statnumber='No';
     $scope.getmachine4 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/numberconfig/",
						params:{"number" : $scope.confnumber},
						 }).then(function(response) {
								   $scope.statnumber= response.data.statnumber;

			});  }				
			
    $scope.firewall='status firewall';
	$scope.route='default route';
	
    $scope.cpu='cpu usage';
	$scope.disk='usage disk';
	$scope.volfile='voluminous file';
    $scope.servicedhcp='status service dhcp';
    $scope.servicedns='status service dns';
    $scope.servicentp='status service ntp';
    $scope.servicefree='status service Freeswitch'
	$scope.delay = 'status';
	$scope.input = "enter the process name";
    $scope.name = 'pid number';
	
	$scope.getmachine1 = function() {
		
			  $http({
						method : "GET",
						url : "/monitoring_app/statusfirewall/",
						 }).then(function(response) {
								   $scope.firewall= response.data.firewall;
						  });
			  $http({
                    method : "GET",
                    url : "/monitoring_app/services/", 
                   }).then(function(response) {
                             $scope.servicedhcp= response.data.dhcpstatus;
                             $scope.servicedns= response.data.dnsstatus;
                             $scope.servicentp= response.data.ntpstatus;
                              $scope.servicefree= response.data.freestatus;
                     });
              
			  
			  
			   $http({
                  method : "GET",
                  url : "/monitoring_app/cpu/",
                  }).then(function(response) {

                          $scope.cpu= response.data.cpu;
                  });
			  $http({
                      method : "GET",
                      url : "/monitoring_app/getpid/",
                      params:{"pidname" :$scope.input},
                       }).then(function (response) {
                                $scope.name = response.data.pidname;
                        });
				

				$http({
                  method : "GET",
                  url : "/monitoring_app/route/",
                  }).then(function(response) {

                          $scope.route= response.data.route;
                  });
    
          $http({
                  method : "GET",
                  url : "/monitoring_app/disk/",
                  }).then(function(response) {

                          $scope.disk= response.data.disk;
                  });

          $http({
                  method : "GET",
                  url : "/monitoring_app/voluminousfile/",
                  }).then(function(response) {

                          $scope.volfile= response.data.volfile;
                  });
           
            $http({
                      method : "GET",
                      url : "/monitoring_app/delay/",
                       }).then(function(response) {
                              $scope.delay= response.data.delay;
                        });}
    
            }]);
})();


