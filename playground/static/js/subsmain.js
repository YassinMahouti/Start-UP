// static/main.js

console.log("check!");

// Get Stripe publishable key
fetch("/playground/config/")
.then((result) => { 
    console.log(result);
    return result.json();})
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  let submitBtn = document.querySelector("#goldBtn");
  let submitBtnSilver = document.querySelector("#SilverBtn");
  let submitBtnBronze = document.querySelector("#BronzeBtn");


  if (submitBtn !== null) {
    submitBtn.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/playground/create-checkout-session/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }

  if (submitBtnSilver !== null) {
    submitBtnSilver.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/playground/create-checkout-session-silver/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }

  if (submitBtnBronze !== null) {
    submitBtnBronze.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/playground/create-checkout-session-bronze/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }

});