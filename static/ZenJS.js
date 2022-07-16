/*.style.display = 'block';*/
let firstwidth;
window.onresize = reportWindowSize;

window.onload = function() {
    firstwidth =  window.innerWidth;
    let aID = document.title.replaceAll(' ', '_');
    document.getElementById(aID).classList.add("chosen");

    //For Card Number formatted input
    let cardNum = document.getElementById('cr_no');
    if(cardNum != null){
        cardNum.onkeyup = function (e) {
    if (this.value == this.lastValue) return;
    let caretPosition = this.selectionStart;
    let sanitizedValue = this.value.replace(/[^0-9]/gi, '');
    let parts = [];

    for (let i = 0, len = sanitizedValue.length; i < len; i += 4) {
        parts.push(sanitizedValue.substring(i, i + 4));
    }

    for (let i = caretPosition - 1; i >= 0; i--) {
        let c = this.value[i];
        if (c < '0' || c > '9') {
            caretPosition--;
        }
    }
    caretPosition += Math.floor(caretPosition / 4);

    this.value = this.lastValue = parts.join(' ');
    this.selectionStart = this.selectionEnd = caretPosition;
    }
    }

    //For Phone Number formatted input #TODO
    let phoneNum = document.getElementById('phone');
    if(phoneNum != null){
        phoneNum.onkeyup = function (e) {
    if (this.value == this.lastValue) return;
    let caretPosition = this.selectionStart;
    let sanitizedValue = this.value.replace(/[^0-9]/gi, '');
    let parts = sanitizedValue;

    this.value = this.lastValue = parts;
    this.selectionStart = this.selectionEnd = caretPosition;
    }
    }


    //For Date formatted input
    let expDate = document.getElementById('exp');
    if(expDate != null){
        expDate.onkeyup = function (e) {
    if (this.value == this.lastValue) return;
    let caretPosition = this.selectionStart;
    let sanitizedValue = this.value.replace(/[^0-9]/gi, '');
    let parts = [];

    for (let i = 0, len = sanitizedValue.length; i < len; i += 2) {
        parts.push(sanitizedValue.substring(i, i + 2));
    }

    for (let i = caretPosition - 1; i >= 0; i--) {
        let c = this.value[i];
        if (c < '0' || c > '9') {
            caretPosition--;
        }
    }
    caretPosition += Math.floor(caretPosition / 2);

    this.value = this.lastValue = parts.join('/');
    this.selectionStart = this.selectionEnd = caretPosition;
    }
    }
}

function reportWindowSize(){
    let width = window.innerWidth;
    let x = document.querySelectorAll(".navL");
    /* if user resized to desktop view from mobile view*/
    if((width > 768) && (firstwidth < 768)){
        for (let i = 0; i < x.length; i++){
            x[i].style.display='inline-block';
        }
    }
    /* if user resized from desktop view to mobile view*/
    if((width < 768) && (firstwidth > 768)){
        for (let i = 0; i < x.length; i++){
            x[i].style.display='none';
        }
    }
    firstwidth =  window.innerWidth;
}

function openMenu() {
    let x = document.querySelectorAll(".navL");
    if(x[0].style.display==='inline-block'){
        for (let i = 0; i < x.length; i++){
            x[i].style.display='none';
        }
    }
    else{
        for (let i = 0; i < x.length; i++){
            x[i].style.display='inline-block';
        }
    }
}

function fetch_ajax(user_id){
    url= 'https://reqres.in/api/users/' + user_id
    fetch(url)
    .then(response => response.json())
    .then(responseJSON => {
        json_dict = responseJSON.data;

        const el = document.createElement('div');
        el.classList.add('glass', 'card', 'glassy2');
        document.getElementsByClassName('formArticle')[0].appendChild(el);

        const h_id = document.createElement('h1');
        h_id.textContent = "id: " + json_dict['id'];
        const name = document.createElement('h1');
        name.textContent = "name: " + json_dict['first_name'] + ' ' + json_dict['last_name'];
        const email = document.createElement('h1');
        email.textContent = "email: " + json_dict['email'];
        const image = document.createElement('img');
        image.src = json_dict['avatar'];

        el.appendChild(h_id);
        el.appendChild(name);
        el.appendChild(email);
        el.appendChild(document.createElement('br'));
        el.appendChild(image);
    })
    .catch(err => console.log(err));
}