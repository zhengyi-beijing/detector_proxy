
import QtQuick 1.0
Rectangle {
    id: window
    width: 800
    height: 600
    //anchors.fill: parent
    color: "lightblue"
    /*
    gradient: Gradient {
         GradientStop { position: 0.0; color: "lightblue" }
         GradientStop { position: 1.0; color: "blue" }
        }*/
    function set_scanner_battery_level (level){
        
    }
    
    function set_xray_battery_level(level) {
    }
    
    function set_detector_running (running) {
            runing_status.running = running
    }
    
    function set_detector_connected(connected) {
        if (connected) {
            detector_connection.source = "res\\CONNECTED.png"
        } else {
            detector_connection.source = "res\\UNCONNECTED.png"
        }
    }
    
    function set_xray_connected(connected) {
        if (connected) {
            xray_connection.source = "res\\CONNECTED.png"
        } else {
            xray_connection.source = "res\\UNCONNECTED.png"
        }
    }
    
    function set_speaker_status (on) {
        if(on) {
            speaker.source = "res\\PCS-EN.png"
        } else {
            speaker.source = "res\\PCS-DI.png"
        }
    }

    function set_stop_status (stopped) {
        if (stopped) {
            stopped.source = "res\\ES-EN.png"
        } else {
            stopped.source = "res\\ES-LK.png"
        }
    }

    function set_trace_info(msg) {
        log.text = msg
    }
    

    
    Column {
        spacing: 2
        //anchors.fill: parent
        height:parent.height
        Rectangle {
            id: title_area
            height: parent.height/6
            width : parent.width
            color:"transparent"
            
            Image {
                anchors.fill:parent
                anchors.margins : 20
                anchors.horizontalCenter : title_area.horizontalCenter
                //anchors.baseline : title_area.verticalCenter

                id: appons
                source:"res\\Appons-With_R1.png"
            }
        }
        Row {
                width: window.width
                height:window.height - title_area.height-status_system.height
                //color:"green"
                Item {
                    width:200
                    height:parent.height
                    id:battery_xray_info
                    //color:"yellow"
                    BatteryBar {
                        id: xray_battery
                        width:parent.width
                        height:300
                        anchors.horizontalCenter : parent.horizontalCenter

                    }
                    
                    Image { 
                        id: xray_connection
                        height :80
                        width : 80
                        fillMode: Image.PreserveAspectFit
                        source: "res\\CONNECTED.png"
                        anchors.horizontalCenter : parent.horizontalCenter
                        anchors.bottom:parent.bottom

                    }
                }
                
                Item {
                    width: parent.width-battery_xray_info.width-battery_detector_info.width
                    height: parent.height
                    AnimatedCircle {
                        id: runing_status
                        color:"transparent"
                        //height:window.height - title_area.height
                        height: parent.height - log.height
                        width: parent.width
                    }
                    

                }
                
                Item {
                    width:battery_xray_info.width
                    height:parent.height
                    id: battery_detector_info
                    //color:"red"
                    BatteryBar {
                        id: detector_battery
                        width:parent.width
                        height:300
                        anchors.horizontalCenter : parent.horizontalCenter
                    }
                    
                    Image { 
                        id: detector_connection
                        height :80
                        width : parent.width
                        fillMode: Image.PreserveAspectFit
                        source: "res\\CONNECTED.png"
                        anchors.horizontalCenter : parent.horizontalCenter
                        anchors.bottom:parent.bottom
                    }
                }
             }

        Item {
                id: status_system
        //        anchors.bottom:parent.bottom
                width:parent.width
                height:80
               // color:"red"

                Text {
                    id: log
                    height: parent.height
                    width: parent.width-stopped.width-speaker.width
                    text: "Waiting"
                    font.pointSize:24
                    anchors.left: parent.left
                    anchors.margins: 10
                }

                Image {
                    id: stopped
                    height : parent.height
                    width : height
                    fillMode: Image.PreserveAspectFit
                    source: "res\\ES-EN.png"
                    //source: "res\\CONNECTED.png"
                    //anchors.bottom: parent.bottom
                    anchors.right: speaker.left
                }

                Image {
                    id: speaker
                    height : parent.height
                    width : height
                    fillMode: Image.PreserveAspectFit
                    source: "res\\PCS-DI.png"
                    //anchors.bottom: parent.bottom
                    anchors.right: parent.right
                }
            }


    }
}
