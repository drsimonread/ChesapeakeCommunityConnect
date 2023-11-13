
// Google Sign-In Callback
function onSignIn(googleUser) {
    // Handle the sign-in logic here
    console.log("User is signed in.");
}
// JavaScript for handling Google Sign-In using One Tap
window.onload = function () {
    google.accounts.id.initialize({
        client_id: "221198763427-g67flvpi5mfvqlhh0a2je4517io0ngkc.apps.googleusercontent.com", // Replace with your client ID
        callback: handleCredentialResponse
    });
    google.accounts.id.renderButton(
        document.getElementById("buttonDiv"),
        { theme: "outline", size: "large" }
    );
    google.accounts.id.prompt();
}

function handleCredentialResponse(response) {
    // Handle the Google Sign-In response here
    // Typically, you would send this response to your server for verification
    console.log("Encoded JWT ID token: " + response.credential);
}