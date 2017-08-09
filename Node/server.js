'use strict';

var arduino = undefined;
var android = undefined;
var sweepPort = undefined;

var SerialPort = require('serialport');
var autonomous=false;


const sweepjs = require('.');
var util = require('util')
var WebSocket = require('ws');
const wss = WebSocket.Server({port: 5001});

//const portName = process.argv[2];
var sweep = undefined;


//var speed = sweep.getMotorSpeed();
//console.log(util.format('Motor speed: %d Hz', speed));

//var rate = sweep.getSampleRate();
//console.log(util.format('Sample rate: %d Hz', rate))

function sleep(millis)
{
    var date = new Date();
    var curDate = null;
    do { curDate = new Date(); }
    while(curDate-date < millis);
}

function doScan(ws)
{
  sweep.scan((err, samples) => 
  {
    if (err)
    {
      console.log("what "+err);
    }
    else
    {
      //console.log("scan");
      
      //ws.send(samples, error => {/**/});
      //samples.command="scan";
      //console.log("samples "+samples.length);
      var msg={command:"scan",samples:samples};
      ws.send(JSON.stringify(msg),error => {/**/})
      

      //samples.forEach((sample) => 
      //{
        // x = cos(angle) * distance
        // y = sin(angle) * distance
        //const msg = {angle: sample.angle, distance: sample.distance};
        //console.log(msg.angle+" "+msg.distance);
        //ws.send(JSON.stringify(msg), error => {/**/});
      //});


      }

  });
}


wss.on('connection', ws => {
  console.log("connected to websocket");

  ws.onclose = evt =>
  {
    console.log("onclose");
  }

ws.on('message', function incoming(data) {
  var msg = JSON.parse(data);
  if(msg.command=="startScanning")
    {
      if( sweep==undefined )
      {
        console.log('Connecting to Sweep on '+sweepPort);
        sweep=new sweepjs.Sweep(sweepPort);

        sweep.setMotorSpeed(3);
        sweep.setSampleRate(1000);
      }
      else
      {
        console.log('Reconnecting to Sweep on '+sweepPort);
      }
      console.log("startScanning");
      sweep.startScanning();
      doScan(ws);
      //intervalId=setInterval(doScan, 10);
    }
    else if(msg.command=="stopScanning")
    {
      console.log("stopScanning");
      //clearInterval(intervalId)
      sweep.stopScanning();
    }
    else if(msg.command=="scan")
    {
      //console.log("scan");
      doScan(ws);
    }
    else if(msg.command=="throttleServo")
    {
      if(autonomous)
      {
        var cmd='T'+msg.value;
        console.log("throttleServo "+cmd);
        arduino.write(cmd+'\n', function(err) { if (err) {console.log('Error on write: ', err.message); } });
      }
    }
    else if(msg.command=="steeringServo")
    {
      if( autonomous )
      {
        var cmd='S'+msg.value;
        console.log("steeringServo "+cmd);
        arduino.write(cmd+'\n', function(err) { if (err) {console.log('Error on write: ', err.message); } });
      }
    }
    else if(msg.command=="sweepPort")
    {
      sweepPort=msg.value;
      console.log("sweepPort " + sweepPort)
    
    }
    else if(msg.command=="androidPort")
    {
      var androidPort=msg.value;
      console.log("androidPort " + androidPort)
      android = new SerialPort(androidPort, {  baudRate: 115200 });
      android.on('data', function (data) 
      {
        autonomous=!!(data[3]&16);
        //console.log("autonomous ",autonomous)

        {
        var cmd='T'+data[1]+'\n';
        //console.log("throttleServo "+cmd);
        arduino.write(cmd, function(err) { if (err) {console.log('Error on write: ', err.message); } });
        }
		
		if(!autonomous)
        {
        var cmd='S'+data[2]+'\n';
        //console.log("steeringServo "+cmd);
        arduino.write(cmd, function(err) { if (err) {console.log('Error on write: ', err.message); } });
        }


      });
    }
    else if(msg.command=="arduinoPort")
    {
      var arduinoPort=msg.value;
      console.log("arduinoPort " + arduinoPort)
      arduino = new SerialPort(arduinoPort, {  baudRate: 115200 });
    }
    else
    {
      console.log("msg "+msg);
    }
});


});





