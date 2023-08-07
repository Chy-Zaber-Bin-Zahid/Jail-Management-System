function editUser(u1, u2, u3, u4, index) {
  document.querySelectorAll(`.staff-details`).forEach((element) => {
    element.style.backgroundColor = "aliceblue";
    element.style.color = "black";
  });
  document.querySelector(".name").value = u2;
  document.querySelector(".email").value = u4;
  document.querySelector(".op").value = u3;
  document.querySelectorAll(`.row-${index}`).forEach((element) => {
    element.style.backgroundColor = "black";
    element.style.color = "white";
  });
}

function editDeputy(u1, index) {
  document.querySelectorAll(`.staff-details`).forEach((element) => {
    element.style.backgroundColor = "aliceblue";
    element.style.color = "black";
  });
  document.querySelector(".email").value = u1;
  
  document.querySelectorAll(`.row-${index}`).forEach((element) => {
    element.style.backgroundColor = "black";
    element.style.color = "white";
  });
}

function editPrisoner(u1, u2, u3, u4, u5, u6, u7, index) {
  document.querySelectorAll(`.staff-details`).forEach((element) => {
    element.style.backgroundColor = "aliceblue";
    element.style.color = "black";
  });
  document.querySelector(".name").value = u2;
  document.querySelector(".age").value = u3;
  document.querySelector(".birth").value = u4;
  document.querySelector(".record").value = u5;
  document.querySelector(".cell").value = u6;
  document.querySelector(".year").value = u7;
  document.querySelectorAll(`.row-${index}`).forEach((element) => {
    element.style.backgroundColor = "black";
    element.style.color = "white";
  });
}

const change = (num) => {
  if (num === 1) {
    document.querySelector(".change-schedule").style.display = "block";
    document.querySelector(".section-schedule").style.filter = "blur(5px)";
    document.querySelector(".section-schedule").style.backgroundColor =
      "#ffffff90";
  } else {
    document.querySelector(".change-schedule").style.display = "none";
    document.querySelector(".section-schedule").style.filter = "blur(0px)";
    document.querySelector(".section-schedule").style.backgroundColor = '';
  }
};

// const request = (num) => {
//   let form = document.querySelector('.form-' + num);
//   form.parentNode.removeChild(form);
// }
