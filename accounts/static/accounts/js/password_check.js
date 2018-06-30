
function checkPass() {
var a = document.getElementById("password1").value;
var b = document.getElementById("password2").value;
var acheck = /^^(?=.*?[a-z])(?=.*?[0-9]).{8,}$/
if (a==="") {
document.getElementById("message").innerHTML="Please fill password!";
return false;
}
if (acheck.test(a)) {
document.getElementById("message").innerHTML=" ";
} else{
document.getElementById("message").innerHTML="Password must be at least 8 in length and contain one number";
return false;
}
if (a==="") {
document.getElementById("message").innerHTML="Please fill password!";
return false;
}
if (a !== b) {
document.getElementById("messages").innerHTML="Confirm password did not match ";
return false;
}
}
