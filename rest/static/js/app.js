/*
 * jQuery File Upload Plugin Angular JS Example 1.2.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, regexp: true */
/*global window, angular */

(function () {
    'use strict';


    //var isOnGitHub = window.location.hostname === 'blueimp.github.io',
    var isOnGitHub = true,
        url = '/productos/uploadImage',
        urlview = '/productos/view/';

    angular.module('demo', [
        'blueimp.fileupload'
    ])
        .config([
            '$httpProvider', 'fileUploadProvider',
            function ($httpProvider, fileUploadProvider) {
                delete $httpProvider.defaults.headers.common['X-Requested-With'];
                fileUploadProvider.defaults.redirect = window.location.href.replace(
                    /\/[^\/]*$/,
                    '/cors/result.html?%s'
                );

                if (isOnGitHub) {
                    // Demo settings:
                    angular.extend(fileUploadProvider.defaults, {
                        // Enable image resizing, except for Android and Opera,
                        // which actually support image resizing, but fail to
                        // send Blob objects via XHR requests:
                        disableImageResize: /Android(?!.*Chrome)|Opera/
                            .test(window.navigator.userAgent),
                        maxFileSize: 5000000,
                        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
                    });
                }
            }
        ])

        .controller('DemoFileUploadController', [
            '$scope', '$http', '$filter', '$window',
            function ($scope, $http) {
                $scope.options = {
                    url: url
                };
                if (!isOnGitHub) {
                    $scope.loadingFiles = true;
                    $http.get(urlview)
                        .then(
                            function (response) {
                                $scope.loadingFiles = false;
                                $scope.queue = response.data.files || [];
                            },
                            function () {
                                $scope.loadingFiles = false;
                            }
                        );
                }
            }
        ])

        .controller('FileDestroyController', [
            '$scope', '$http',
            function ($scope, $http) {
                var file = $scope.file,
                    state;
                if (file.url) {
                    file.$state = function () {
                        return state;
                    };
                    file.$destroy = function () {
                        state = 'pending';
                        return $http({
                            url: file.deleteUrl,
                            method: file.deleteType,
                            xsrfHeaderName: 'X-CSRFToken',
                            xsrfCookieName: 'csrftoken'
                        }).then(
                            function () {
                                state = 'resolved';
                                $scope.clear(file);
                                $scope.colaClass.splice(0,1);
                            },
                            function () {
                                state = 'rejected';
                            }
                        );
                    };
                } else if (!file.$cancel && !file._index) {
                    file.$cancel = function () {
                        $scope.clear(file);
                    };
                }
            }
        ])

        .controller('FileClassificationController', [
            '$scope', '$http',
            function ($scope, $http) {
                var file = $scope.file,
                state;

                if (file.url) {
                    file.$state = function() {
                        return state;
                    }
                    file.$classification = function() {
                        state = 'pending';
                        var arrayUrl = file.deleteUrl.split('/');
                        arrayUrl[2] = "classificationImage";

                        var newUrl = arrayUrl.join('/');

                        var peticion = $http({
                            url: newUrl,
                            method: 'POST',
                            xsrfHeaderName: 'X-CSRFToken',
                            xsrfCookieName: 'csrftoken'
                        });

                        peticion.success(function(data) {
                            console.log(data);
                        });
                        
                        return peticion.then(
                            function() {
                                state = 'resolved';
                            },
                            function() {
                                state = 'rejected';
                            }
                        );
                    };
                }
            }
        ])

        .controller('FileClassificationAllController', [
            '$scope', '$http',
            function ($scope, $http) {
                $scope.all = function() {
                    console.log('all controller')
                }
            }
        ]);

}());
