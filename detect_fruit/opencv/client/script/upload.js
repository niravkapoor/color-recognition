
function _init() {
  document.getElementById("defaultOpen").click();
  if (!window.localStorage.getItem("phone")) {
    document.getElementById("myModal").style.display = "block";
    
    document.getElementById("cntBox").style.display = "none";
  } else {
    document.getElementById("cntBox").style.display = "block";
    
    document.getElementById("myModal").style.display = "none";
    fetchAllUploads();
  }
}

const verifChange = (id) => {
  try{
    console.log(getCookie("csrftoken"));
    fetch(`/opencv/verify_uploads/${id}`, {
      method: "PUT",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if(data){
        let parent = document.getElementById(`${id}`).parentElement;
        parent.innerHTML = "Already Verified";
      }
    })
    .catch((error) => {
      console.error(error);
      document.getElementById(`${id}`).checked = false
    });
  }
  catch(err){
    document.getElementById(`${id}`).checked = false
  }
}

function submit(event) {
  const formData = new FormData(document.getElementById("form"));
  fetch("/opencv/upload", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
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
        "X-CSRFToken": getCookie("csrftoken"),
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
    myHtmlContent = `
    <td>${data[i].url}</td>
    <td>${data[i].is_verified}</td>
    <td><img src="http://${window.location.host}${data[i].url}"/></td>
    <td>${data[i].fruit_name == null? 'Not Processed' : data[i].fruit_name}</td>
    <td>${!data[i].is_verified? `<input id="${data[i].id}" type="checkbox" onclick="verifChange(${data[i].id});"/>` : 'Already Verified'}</td>
    `
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

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
// Get the element with id="defaultOpen" and click on it
_init();
