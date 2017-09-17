const AuroraApi = require('nanoleaf-aurora-client'),
  ROSLIB = require('roslib');

var api = new AuroraApi({
  host: '192.168.1.103',
  base: '/api/v1/',
  port: '16021',
  accessToken: 'm1LeezHyO8Myo8zvnN59ss9xZHbjNVj9'
});

var ros = new ROSLIB.Ros();

ros.on('connection', function() {
console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
console.log('Connection to websocket server closed.');
});

var resultTopic = new ROSLIB.Topic({
  ros: ros,
  name: '/class',
  messageType: 'std_msgs/String'
});

function connect() {
  api.turnOn()
    .then(function() {
      console.log('Success!');
    })
    .catch(function(err) {
      console.error('test' + err);
    });
}

function setEffect(effect) {
  api.setEffect(effect)
  .then(function() {
    console.log('Success!');
  })
  .catch(function(err) {
    console.error(err);
  });
}

ros.connect("wss://localhost:9090", {
      protocolVersion: 13,
      origin: "https://localhost:8888",
      rejectUnauthorized: false
    });

resultTopic.subscribe(function(msg) {
  if (msg.data == "pick me up") {
    connect();
    setEffect("Color Burst");
  } else if (msg.data == "high five") {
    connect();
    setEffect("Romantic");
  } else if (msg.data == "two side finger") {
    connect();
    setEffect("Northern Lights");
  } else if (msg.data == "no hands") {
    api.turnOff()
      .then(function() {
        console.log('Success!');
      })
      .catch(function(err) {
        console.error('test' + err);
      });
  }
});
