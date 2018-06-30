
function checkPass() {
var a = document.getElementById("password1").value;
var b = document.getElementById("password2").value;
var acheck = /^^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/
if (a==="") {
document.getElementById("message").innerHTML="Please fill password!";
return false;
}
if (acheck.test(a)) {
document.getElementById("message").innerHTML=" ";
} else{
document.getElementById("message").innerHTML="Password must be atleast 8 in lenth and contain one speacial character,number,lower case and upper case alphabet";
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
