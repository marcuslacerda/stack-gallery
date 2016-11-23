app.controller('HomeController', ['$scope', '$http', '$auth', function($scope, $http, $auth) {
    // TODO - use 
    $http.jsonp('https://api.github.com/repos/marcuslacerda/stack-gallery?callback=JSON_CALLBACK')
      .success(function(data) {
        if (data) {
          if (data.data.stargazers_count) {
            $scope.stars = data.data.stargazers_count;
          }
          if (data.data.forks) {
            $scope.forks = data.data.forks;
          }
          if (data.data.open_issues) {
            $scope.issues = data.data.open_issues;
          }
        }
      });
  }]);
