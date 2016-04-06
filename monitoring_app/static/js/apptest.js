(function(){
var app= angular.module('monitoring', []);
app.directive('file', function(){
    return {
        scope: {
            file: '='
        },
        link: function(scope, el, attrs){
            el.bind('change', function(event){
                var files = event.target.files;
                var file = files[0];
				var filePath=$('#file').val();
                scope.file = file ? file.name : undefined;
                scope.$apply();
            });
        }
    };
});
app.controller('monitoringcontroller', ['$scope','$http',  function($scope,$http) {
    $scope.status='click sur Get ';
	$scope.statusge= function($id) {
        $http({
		method : "GET",
		url : "/monitoring_app/statusgeneral/",
	    params:{"id" : $id},
		}).then(function(response) {
			$scope.status=response.data.status;
			
		});			}
		
		 $scope.phone='No numbers';
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
			
	$scope.wavname ='Click in begin to get the .wav file path';
	$scope.pcapfile='insert a name to your pcap file';
	$scope.start = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/makecall/",
						params:{"namepcap" : $scope.pcapfile},
						 }).then(function(response) {
							 		 $scope.wavname= response.data.wavname;
        

			});  }	
	 $scope.confnumber='1000';
	 $scope.statnumber='No';
	 $scope.codec='PCMA';
	 $scope.param = {};
	 
     $scope.getmachine4 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/numberconfig/",
						params:{"number" : $scope.confnumber,"codec" : $scope.codec,"file":$scope.param["file"]},
						 }).then(function(response) {
							 		 $scope.statnumber= response.data.statnumber;
        

			});  }	
			
     $scope.numberconf='1000';
	 $scope.delnumber='No';
     $scope.getmachine5 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/numberdelete/",
						params:{"numbertodelete" : $scope.numberconf},
						 }).then(function(response) {
								   $scope.delnumber= response.data.delnumber;

			});  }				
	 $scope.numbersoft='1500';
	 $scope.statnumbersoft='No';
     $scope.getmachine6 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/numbersoftconfig/",
						params:{"number" : $scope.numbersoft},
						 }).then(function(response) {
								   $scope.statnumbersoft= response.data.statnumber;

			});  }	
			
     $scope.numbersoftremove='1500';
	 $scope.delnumbersoft='No';
     $scope.getmachine7 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/numbersoftdelete/",
						params:{"numbertodelete" : $scope.numbersoftremove},
						 }).then(function(response) {
								   $scope.delnumbersoft= response.data.delnumbersoft;

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


