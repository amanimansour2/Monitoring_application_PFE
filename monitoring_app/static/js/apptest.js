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
			volfile=response.data.volfile;
			delay=response.data.delay;
			dhcpstatus=response.data.dhcpstatus;
			ntpstatus=response.data.ntpstatus;
			dnsstatus=response.data.dnsstatus;
			freestatus=response.data.freestatus;
			disk=response.data.disk;
			cpu=response.data.cpu;
			route=response.data.route;
			
			if (delay =="True"){ 
			  $scope.status ="Not OK !!";
			}else{ 
			if (route =="False"){ 
			  $scope.status ="Not OK !!";
			}else{
			if (dhcpstatus =="OFF"){ 
			  $scope.status ="Not OK !!";
			}else{
			if (ntpstatus =="OFF"){ 
			  $scope.status ="Not OK !!";
			}else{
			if (dnsstatus =="OFF"){ 
			  $scope.status ="Not OK !!";
			}else{
			if (freestatus =="OFF"){ 
			  $scope.status ="Not OK !!";
			}else{
			if (volfile =="True"){ 
			  $scope.status ="Not OK !!";
			}else{
			$scope.status ="OK !!!";} }}}}}}
		});			}
		
		
	 
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


