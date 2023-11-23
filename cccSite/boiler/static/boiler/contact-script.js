
document.addEventListener("DOMContentLoaded", function () {
    const contactTab = document.getElementById("contact-tab");
    const showContactFormButton = document.getElementById("show-contact-form-button");
    const contactForm = document.getElementById("contact-form");

    // Show the contact form when the button is clicked
    showContactFormButton.addEventListener("click", function () {
        showContactFormButton.style.display = "none";
        contactForm.style.display = "block";
    });

    contactForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const message = document.getElementById("message").value;

        const contactData = {
            name,
            email,
            message,
        };

        // Simulate form submission (adjust this part for your server)
        // Assuming a successful submission
        simulateFormSubmission(contactData);
    });

    function simulateFormSubmission(contactData) {
        // Send contactData to the server for saving (simulated with a delay)
        setTimeout(() => {
            // Reset the form
            document.getElementById("name").value = "";
            document.getElementById("email").value = "";
            document.getElementById("message").value = "";

            // Show success message and hide the form
            alert("Contact form submitted successfully!");
            contactTab.style.display = "none";
            showContactFormButton.style.display = "block";
        }, 1000); // Simulated submission delay (1 second)
    }
});
