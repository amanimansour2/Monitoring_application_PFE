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
app.controller('monitoringcontroller', ['$scope','$http', '$log', '$window', function($scope,$http,$log, $window) {
    $scope.status='Status';
	$scope.statusge= function($id) {
        $http({
		method : "GET",
		url : "/monitoring_app/statusgeneral/",
	    params:{"id" : $id},
		}).then(function(response) {
			$scope.status=response.data.status;
			
		});			}
		
    $scope.initialisation='Not yet';
	$scope.initialize = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/initialize/",
						 }).then(function(response) {
								   $scope.initialisation= response.data.initialisation;
			});  }	
		
		
		 $scope.phone='No numbers';
	$scope.getmachine2 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/regphone/",
						 }).then(function(response) {
								   $scope.phone= response.data.phone;
			});  }
	$scope.stat='Not yet';
    $scope.getmachine3 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/freeswitchcommunication/",
						 }).then(function(response) {
								   $scope.stat= response.data.stat;

			});  }
	$scope.selected = 'NO';
	$scope.selectedd = 'NO';
	$scope.selecteddd = 'NO';
	$scope.wavname ='/your/path/to/your/wav ...';
	$scope.intercapture='enp0s8';
	$scope.addcapture='192.168.3.1';
	$scope.timecapture='20';
	$scope.start = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/makecall/",
						params:{"time1":$scope.timecapture},
						 }).then(function(response) {
							 		 $scope.wavname= response.data.wavname;
        

			});  }
	$scope.download = function() {
       var url = "http://" + $window.location.host + "/monitoring_app/downwav/";
       $log.log(url);
       $window.location.href = url;     }
	$scope.telecharger = function() {
       var url = "http://" + $window.location.host + "/monitoring_app/down/";
       $log.log(url);
       $window.location.href = url;     }
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
     $scope.oldname='name';
     $scope.newusername='username';
     $scope.newname='new name';			
     $scope.newaddress='address';			
     $scope.newpassword='password';			
     $scope.newprefix='prefix';				 
     $scope.editmachine = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/pid/edit_machine/",
						params:{"oldname":$scope.oldname,"newname":$scope.newname,"newaddress":$scope.newaddress,"newusername":$scope.newusername,"newpasword":$scope.newpassword,"newprefix":$scope.newprefix},
						 }).then(function(response) {

			});  }			
	$scope.update = function() {
		          $http({
						method : "GET",
						url : "/monitoring_app/pid/edit_machine_DB/",
					   params:{"oldname":$scope.oldname},
						 }).then(function(response) {
	  $scope.newname = $scope.oldname;
      $scope.newaddress = response.data.address;
     $scope.newusername = response.data.username;
     $scope.newpassword = response.data.password;
     $scope.newprefix = response.data.Prefix_freeswitch; 


			});  }	
    
     $scope.namemachine='name';			
     $scope.deletmachine = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/pid/del_machine/",
						params:{"namemachine":$scope.namemachine},
						 }).then(function(response) {

			});  }				
	 $scope.numbersoft='1500';
	 $scope.scenario='None';
	 $scope.adphone="192.168.3.1";
	 $scope.dtmf="0123456789";
	 $scope.statnumbersoft='No';
     $scope.getmachine6 = function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/numbersoftconfig/",
						params:{"number" : $scope.numbersoft,"scenario":$scope.scenario,"adphone":$scope.adphone,"dtmf":$scope.dtmf,"selecteddd":$scope.selecteddd},
						 }).then(function(response) {
								   $scope.statnumbersoft= response.data.statnumber;

			});  }	
	 $scope.numsrc='caller';
	 $scope.numdest='callee';
	 $scope.scenarioinvite='INVITE_with_name';
	 $scope.statcall1='No';
	 $scope.adressphone="192.168.3.1";
	 $scope.dure='0';
	 $scope.interfac='enp0s8';
     $scope.call1= function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/inviteconfig/",
						params:{"numsrc" : $scope.numsrc,"numdest" : $scope.numdest,"scenarioinvite":$scope.scenarioinvite,"addphone":$scope.adressphone,"dure":$scope.dure,"interface":$scope.interfac,"checked":$scope.selected},
						 }).then(function(response) {
								   $scope.statcall1= response.data.statcall1;

			});  }	
	 $scope.numclient='1000';
	 $scope.addclient='192.168.3.9';
	 $scope.scenarioreinvite='Pending_Request';
	 $scope.statcall2='No';
	 $scope.adressphone="192.168.3.1";
	 $scope.dure='0';
	 $scope.interfac='enp0s8';
     $scope.call2= function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/reinviteconfig/",
						params:{"numclient" : $scope.numclient,"addclient" : $scope.addclient,"scenarioreinvite":$scope.scenarioreinvite,"addphone":$scope.adressphone,"dure":$scope.dure,"interface":$scope.interfac,"checked":$scope.selected},
						 }).then(function(response) {
								   $scope.statcall2= response.data.statcall2;

			});  }
     $scope.testscenarioo='No';	
	 $scope.duree='0';
	 $scope.interfacc='enp0s8';
        $scope.testscenario= function() {
			  $http({
						method : "GET",
						url : "/monitoring_app/calltest/",
						params:{"dure":$scope.duree,"interface":$scope.interfacc,"checked":$scope.selectedd},
						 }).then(function(response) {
								   $scope.testscenarioo= response.data.testscenarioo;

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


