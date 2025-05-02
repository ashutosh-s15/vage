const Toastify = require('toastify-js');

function toggleDropdown() {
  var dropdownContent = document.getElementById("dropdown-content");
  dropdownContent.style.display = dropdownContent.style.display === "flex" ? "none" : "flex";
}

function changeBackground(background) {
  console.log("clicked!!")
  toggleDropdown();
}

const dropDownBtn = document.querySelector('.dropdown-btn');
dropDownBtn.addEventListener('click', function () {
  toggleDropdown()
});

// Attach onclick event to background option elements
var backgroundOptions = document.querySelectorAll(".background-option");
backgroundOptions.forEach(function (option) {
  option.onclick = function () {
    var background = option.getAttribute("data-background");
    changeBackground(background);
  };
});

function saveSettingChanges() {

  // var options = {
  //   scriptPath: path.join(__dirname, '/../engine/'),
  // }

  // PythonShell.run('VirtualCanvas.py', options, function (err, results) {
  //   if (err)
  //     throw err;
  //   else
  //     success = true;

  //   console.log('finished: %j', results);
  // });

  Toastify({
    text: "Saved Changes",
    duration: 3000,
    close: false,
    gravity: "bottom",
    position: "right",
    stopOnFocus: true,
    style: {
      position: 'absolute',
      width: '100%',
      background: "linear-gradient(to right, #00b09b, #96c93d)",
      textAlign: 'center',
      padding: '10px 0px'
    },
  }).showToast();

}

const saveBtn = document.querySelector('#cta-save');
saveBtn.addEventListener('click', saveSettingChanges);