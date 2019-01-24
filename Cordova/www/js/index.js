/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
var app = {
    // Application Constructor
    initialize: function() {
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
        document.addEventListener('pause', this.onPause.bind(this), false);
        document.addEventListener('resume', this.onResume.bind(this), false);
    },

    // deviceready Event Handler
    //
    // Bind any cordova events here. Common events are:
    // 'pause', 'resume', etc.
    onDeviceReady: function() {
        console.log("device really ready");

        var paired = true;
        var pass = 123456;


        //Setup Buttons
        var grid_x = 3;
        var grid_y = 5;

        var heightPercent = 100/grid_y;
        var widthPercent = 100/grid_x;
        var buttonCount = grid_x * grid_y;
        
        var buttonContainer = document.getElementById("buttonContainer")
        var buttons = []
        for (let i = 0; i < buttonCount; i++) {
            var btn = document.createElement("BUTTON")
            btn.classList.add("button-wrapper");
            btn.classList.add("button");
            btn.style.width = widthPercent+"%";
            btn.style.height = heightPercent+"%";
            btn.addEventListener("touchstart", this.onKeyPressed.bind(this, i), false);
            btn.addEventListener("touchend", this.onKeyReleased.bind(this, i), false);
            buttons.push(btn)
            buttonContainer.appendChild(btn);
        }

        //Wifi https://github.com/apache/cordova-plugin-network-information

        var zeroconf = cordova.plugins.zeroconf;

        var goneOnlineEntered = false

        document.addEventListener("online", onOnline, false);
        console.log(navigator.connection.type);
        
        function onOnline() {
            // Handle the online event
            console.log("chack");
            
            var networkState = navigator.connection.type;

            if (networkState == Connection.WIFI) {
                if(goneOnlineEntered == true) return;
                goneOnlineEntered = true
                console.log("Connected now")
                setTimeout(function () {
                    discover();
                }, 1000);
                
            }else{
                goneOnlineEntered = false
            }

        }

        //initial wifi check
        if(navigator.connection.type == Connection.WIFI){
            onOnline();
        }

        var zeroconf = cordova.plugins.zeroconf;
        
        function discover(){
            zeroconf.reInit()
            zeroconf.watch('_pmdeck._tcp.', 'local.', function(result) {
                var action = result.action;
                var service = result.service;
                if (action == 'added') {
                    console.log('service added'+ service);
                } else if (action == 'resolved') {
                    console.log('service resolved'+ service.ipv4Addresses[0] + ":" + service.port +";");
                    /* service : {
                    'domain' : 'local.',
                    'type' : '_http._tcp.',
                    'name': 'Becvert\'s iPad',
                    'port' : 80,
                    'hostname' : 'ipad-of-becvert.local',
                    'ipv4Addresses' : [ '192.168.1.125' ], 
                    'ipv6Addresses' : [ '2001:0:5ef5:79fb:10cb:1dbf:3f57:feb0' ],
                    'txtRecord' : {
                        'foo' : 'bar'
                    } */
                    var socket = new Socket();

                    socket.onData = function(data) {
                        // invoked after new batch of data is received (typed array of bytes Uint8Array)
                        
                        stream = new TextDecoder("utf-8").decode(data);
                        stream.split(';').filter(v=>v!='').forEach(function(msg) {
                            console.log(msg);
                            var spl = msg.split(":");
                            var cmd = spl[0];
                            switch (cmd) {
                                case "IMAGE":
                                    var args = spl[1].split(",");
                                    var btn = buttons[args[0]]
                                    url = "data:image/png;base64," + args[1];
                                    btn.style.backgroundImage = "url('" + url.replace(/(\r\n|\n|\r)/gm, "") + "')";
                                    break;
                                case "CONN":
                                    var args = spl[1].split(",")
                                    var dataString = "CONNACCEPT;";
                                    var data = new Uint8Array(dataString.length);
                                    for (var i = 0; i < data.length; i++) {
                                        data[i] = dataString.charCodeAt(i);
                                    }
                                    socket.write(data);

                                default:
                                    break;
                            }
                        });

                    };
                    socket.onError = function(errorMessage) {
                        // invoked after error occurs during connection
                        console.log("ERROR: "+errorMessage);
                        
                    };
                    socket.onClose = function(hasError) {
                        // invoked after connection close
                        console.log("CLOSE: "+hasError);
                        
                    };

                    socket.open(
                        service.ipv4Addresses[0], 
                        service.port,
                        function() {
                            console.log("connected");
                            if(paired){
                                var dataString = "CONN:cordova1;";
                                var data = new Uint8Array(dataString.length);
                                for (var i = 0; i < data.length; i++) {
                                    data[i] = dataString.charCodeAt(i);
                                }
                                socket.write(data);
                            }else{
                                // syncTrying = false;
                                // syncPass = "";
                                // con.sendMessage("SYNCREQ:$uid;");
                            }
                        },
                        function(errorMessage) {
                          // invoked after unsuccessful opening of socket
                          console.log(errorMessage);
                        }
                    );


                } else {
                    console.log('service removed'+ service);
                }
            });
        }
    },

    onPause: function() {
        console.log("Paused");
    },

    onResume: function() {
        console.log("resumed");
    },

    onKeyPressed: function(key) {
        console.log("Key Pressed " + key);

    },

    onKeyReleased: function(key) {
        console.log("Key Released " + key);

    }



};

app.initialize();