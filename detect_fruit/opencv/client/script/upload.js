const files = [];
function _init() {
  document.getElementById("defaultOpen").click();

  // document.querySelector('#fileToUpload').addEventListener('change', event => {
  //     handleImageUpload(event)
  // })
  if (!window.localStorage.getItem("phone")) {
    document.getElementById("myModal").style.display = "block";
    
    document.getElementById("cntBox").style.display = "none";
    // document.getElementById("fetchBtn").style.display = "none";
    // document.getElementById("phnDiv").style.display = "block";
  } else {
    // document.getElementById("form").style.display = "block";
    document.getElementById("cntBox").style.display = "block";
    
    document.getElementById("myModal").style.display = "none";
    fetchAllUploads();
    // document.getElementById("phnDiv").style.display = "none";
  }
}

function handleImageUpload(event) {
  files.push(event.target.files);
}

function submit(event) {
  // const files = event.target.files;
  const formData = new FormData(document.getElementById("form"));
  // formData.append('filedata', "acx")
  fetch("/opencv/upload", {
    method: "POST",
    headers: {
      "X-CSRFToken": document.cookie.split("csrftoken=")[1],
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error(error);
    });
}

function getDetails() {
  let phone = document.getElementById("phnNum").value;
  if (phone) {
    fetch(`/opencv/details/${phone}`, {
      method: "GET",
      headers: {
        "X-CSRFToken": document.cookie.split("csrftoken=")[1],
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        window.localStorage.setItem("user_id", data.data.user_id);
        window.localStorage.setItem("phone", phone);
        document.getElementById("cntBox").style.display = "block";
    
        document.getElementById("myModal").style.display = "none";
        fetchAllUploads();
      })
      .catch((error) => {
        console.error(error);
      });
  }
}

function fetchAllUploads() {
  let user_id = window.localStorage.getItem("user_id");
  if (user_id) {
    fetch(`/opencv/get_uploads/${user_id}`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        addRows(data.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }
}

function addRows(data) {
  let myHtmlContent = "";
  let tableRef = document.getElementById('uploads').getElementsByTagName('tbody')[0];
  for(let i =0; i < data.length; i++){
    myHtmlContent = `<td>${data[i].url}</td><td>${data[i].is_verified}</td><td><img /></td>`
    let newRow = tableRef.insertRow(tableRef.rows.length);
    newRow.innerHTML = myHtmlContent;
  }
}

function openPage(pageName,elmnt,color) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }
  document.getElementById(pageName).style.display = "block";
  elmnt.style.backgroundColor = color;
}

// Get the element with id="defaultOpen" and click on it
_init();
