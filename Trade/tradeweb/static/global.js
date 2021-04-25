function my(id) {
    return document.getElementById(id);
}

my("add_btn").onclick = function () {

    my("changeblock").style.display = "";
}
my("cancle").onclick = function () {
    my("changeblock").style.display = "none";
}