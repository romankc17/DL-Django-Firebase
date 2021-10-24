
// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
//var firebaseConfig = {
//    apiKey: "AIzaSyC0xnr3u6UdBSr8B92RrmuhSHHWOxoyEWU",
//    authDomain: "drivingliscence-72223.firebaseapp.com",
//    databaseURL: "https://drivingliscence-72223-default-rtdb.firebaseio.com",
//    projectId: "drivingliscence-72223",
//    storageBucket: "drivingliscence-72223.appspot.com",
//    messagingSenderId: "590919060724",
//    appId: "1:590919060724:web:f467b1e6f946d44a15a2a1",
//    measurementId: "G-TZWEBNE6SN"
//};
//// Initialize Firebase
//firebase.initializeApp(firebaseConfig);
//firebase.analytics();
//
//const storage = firebase.storage()
//const db = firebase.firestore();
//db.settings({timestampsInSnapshots: true});

const items = [
{
    id:'1',
    email:'roman@gmail.com',
    displayName:'Roman KC',
    staff:'True',
},
{
    id:'2',
    email:'roman@gmail.com',
    displayName:'Roman KC',
    staff:'True',
},
{
    id:'3',
    email:'roman@gmail.com',
    displayName:'Roman KC',
    staff:'True',
},
{
    id:'4',
    email:'roman@gmail.com',
    displayName:'Roman KC',
    staff:'True',
},

]

function deleteFunc(id){
    if (confirm("Are you sure, you want to delete "+id)) {
        txt = "You pressed OK!";
    }
}

function editFunc(id){

}

function loadTable(items){
    let table = document.getElementById("tbBody")
    items.forEach(item => {
        let row = table.insertRow();
        let id = row.insertCell(0);
        let email = row.insertCell(1);
        let displayName = row.insertCell(2);
        let staff = row.insertCell(3);
        let edit_icon = row.insertCell(4)
        let delete_icon = row.insertCell(5)

        id.innerHTML = item.id;
        email.innerHTML = item.email;
        displayName.innerHTML = item.displayName;
        staff.innerHTML = item.staff;
        edit_icon.innerHTML = `<button onclick='editFunc(${item.id})'><i class='fa fa-edit'></i></button>`
        delete_icon.innerHTML = `<button onclick='deleteFunc(${item.id})'><i class='fa fa-trash'></i></button>`

    });
}

loadTable(items)
