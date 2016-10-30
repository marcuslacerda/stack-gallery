app.controller('AppCtrl', ['$scope', '$mdBottomSheet','$mdSidenav', '$mdDialog', '$resource', '$timeout', function($scope, $mdBottomSheet, $mdSidenav, $mdDialog, $resource, $timeout){

  $scope.input = ''

  $scope.searchAll = function() {
    $scope.input = ''
    Stack.list(function(data){
      $scope.projects = data;         
    });    
  }

  $scope.search = function() {

    q = $scope.input
    if (q == '' || q == null) {
      q = "*"
    }

    Stack.search({ q: q }, function(data){
      $scope.projects = data;
    });
  };

  $scope.keyPress = function(event){
    console.log(event.keyCode + ' - ' + event.altKey);
    // if keyCode = ENTER (#13) 
    if (event.altKey && event.keyCode == 70) {
      $scope.showSearch = true
      $timeout(function () { 
              document.getElementById('search_input').focus();
      }, 10);      
    }

    if ($scope.showSearch) { 
      if (event.keyCode == 13) {
        $scope.search()
      }
      // if keyCode = ESC (#27)
      if (event.keyCode == 27) {
        $scope.showSearch = false
      }
    }
  };

  var Stack = $resource('api/stack/:action', 
      { q : '@q' }, 
      {
        list : { method : 'GET', isArray: true },
        search : { method : 'GET', params : {action : 'search'}, isArray: true }
      }
  );

  //var StackApi = $resource('stack');
  Stack.list(function(data){
    $scope.projects = data;         
  });

  $scope.showTeam = function(ev, stack_id) {

    // GET team for stack id
    url = 'stack/team/' + stack_id
    var TeamApi = $resource(url);
    TeamApi.query(function(data){
      $mdDialog.show({
        controller: DialogController,
        templateUrl: 'dialog-team',
        targetEvent: ev,
        locals : {team : data},
        clickOutsideToClose: true,
        escapeToClose: true
      })
      .then(function(answer) {
        $scope.alert = 'You said the information was "' + answer + '".';
      }, function() {
        $scope.alert = 'You cancelled the dialog.';
      });
    });  
  };

  $scope.likeCount = 2

  $scope.like = function(item) {
    item.like_count += 1
    console.log('TODO: async call to update like action' + item.key)
  }

}]);

function DialogController($scope, $mdDialog, team) {
  $scope.team =  team

  $scope.hide = function() {
    $mdDialog.hide();
  };
  $scope.cancel = function() {
    $mdDialog.cancel();
  };
  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };
};