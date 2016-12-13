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

    //angular.module('demo', ['angular-loading-bar', 'ngAnimate'])
    angular.module('demo', [
        'blueimp.fileupload',
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
                    colaClass = $scope.colaClass,
                    multipleData = $scope.multipleData,
                    learningData = $scope.learningData,
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

                                for(var i = 0; i < colaClass.length; i++) {
                                    if(colaClass[i] === file.name) {
                                        colaClass.splice(i,1);
                                        break;
                                    }
                                }

                                for(var i = 0; i < multipleData.length; i++) {
                                    if(multipleData[i].imagen === file.name) {
                                        multipleData.splice(i,1);
                                        break;
                                    }
                                }

                                learningData.splice(0,1);
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
                    solicitud = $scope.solicitud,
                    multipleData = $scope.multipleData,
                    learningData = $scope.learningData,
                    tiempo = $scope.tiempo,
                    state;

                if (file.url) {
                    file.$state = function() {
                        return state;
                    }
                    file.$classification = function() {
                        state = 'pending';
                        solicitud.push(0);
                        multipleData.splice(0,multipleData.length);
                        learningData.splice(0,learningData.length);

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
                            solicitud.splice(0,1);

                            //multipleData.push(data);

                            console.log(data);

                            tiempo.splice(0,1);
                            tiempo.push(data.tiempo);

                            for(var i = 0; i < data.multiple.length; i++) {
                                multipleData.push(data.multiple[i]);
                            }
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

        .controller('FileMultipleClassificationController', [
            '$scope', '$http',
            function ($scope, $http) {
                var dataImages = $scope.colaClass,
                    solicitud = $scope.solicitud,
                    multipleData = $scope.multipleData,
                    learningData = $scope.learningData,
                    tiempo = $scope.tiempo;

                $scope.multiple = function() {
                    solicitud.push(0);
                    multipleData.splice(0,multipleData.length);
                    learningData.splice(0,learningData.length);

                    console.log(dataImages);

                    var peticion = $http({
                        url: 'multipleClassification',
                        method:'POST',
                        data: dataImages,
                        xsrfHeaderName: 'X-CSRFToken',
                        xsrfCookieName: 'csrftoken'
                    });

                    peticion.success(function(data) {
                        solicitud.splice(0,1);

                        //multipleData.push(data);

                        console.log(data);

                        tiempo.splice(0,1);
                        tiempo.push(data.tiempo);

                        for(var i = 0; i < data.multiple.length; i++) {
                            multipleData.push(data.multiple[i]);
                        }
                    });
                }
            }
        ])

        .controller('FileLearningController', [
            '$scope', '$http',
            function ($scope, $http) {
                var file = $scope.file,
                    solicitud = $scope.solicitud,
                    multipleData = $scope.multipleData,
                    learningData = $scope.learningData,
                    tiempo = $scope.tiempo,
                    state;

                if (file.url) {
                    file.$state = function() {
                        return state;
                    }
                    file.$learning = function() {
                        state = 'pending';
                        solicitud.push(0);
                        multipleData.splice(0,multipleData.length);
                        learningData.splice(0,learningData.length);

                        var arrayUrl = file.deleteUrl.split('/');
                        arrayUrl[2] = "learningImage";

                        var newUrl = arrayUrl.join('/');

                        var dataLayers = ['conv1','conv2','conv3','conv4','conv5'];

                        /*                        
                        'pool1','pool2','pool5',
                        'norm1','norm2'];
                        */

                        var peticion = $http({
                            url: newUrl,
                            method: 'POST',
                            data: dataLayers,
                            xsrfHeaderName: 'X-CSRFToken',
                            xsrfCookieName: 'csrftoken'
                        });

                        peticion.success(function(data) {
                            solicitud.splice(0,1);

                            console.log(data);

                            tiempo.splice(0,1);
                            tiempo.push(data.tiempo);

                            learningData.push(data);
                        });
                        
                        return peticion.then(
                            function() {
                                state = 'resolved';
                            },
                            function() {
                                state = 'rejected';
                            }
                        );
                    }
                }
            }
        ]);

}());
