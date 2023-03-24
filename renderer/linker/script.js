const path = require("path");
const { PythonShell } = require('python-shell');
const Toastify = require('toastify-js');

// function startVirtualCanvas() {

//   var options = {
//     scriptPath: path.join(dir.cwd(), '/engine/'),
//   }

//   PythonShell.run('VirtualCanvas.py', options, function (err, results) {
//     if (err) throw err;
//     console.log('finished: %j', results);
//   });

// }

function startVirtualCanvas() {

  var options = {
    scriptPath: path.join(__dirname, '/../engine/'),
  }

  PythonShell.run('VirtualCanvas.py', options, function (err, results) {
    if (err)
      throw err;
    else
      success = true;

    console.log('finished: %j', results);
  });

  Toastify({
    text: "Launching Virtual Canvas. Please wait.",
    duration: 12000,
    close: false,
    gravity: "bottom",
    position: "right",
    stopOnFocus: true,
    style: {
      position: 'absolute',
      width: '50%',
      background: "linear-gradient(to right, #00b09b, #96c93d)",
      textAlign: 'center',
      padding: '10px 0px'
    },
  }).showToast();

}

const btn = document.querySelector('#cta-start');
btn.addEventListener('click', startVirtualCanvas);