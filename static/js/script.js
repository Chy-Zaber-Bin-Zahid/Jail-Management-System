function editUser(u1, u2, u3, u4, index) {
  document.querySelectorAll(`.staff-details`).forEach(element => {
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
function editPrisoner(u1, u2, u3, u4, u5, u6, u7, index) {
  document.querySelectorAll(`.staff-details`).forEach(element => {
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
