const getUserId = () => {
  let userId = 0;
  const navCartQuantity = document.querySelector(".nav-side--link-quantity");
  if (navCartQuantity && navCartQuantity.dataset.userId)
    userId = navCartQuantity.dataset.userId;
  return userId;
};

const getCartItems = () => {
  const userId = getUserId();
  const cart = JSON.parse(localStorage.getItem("cart")) || {};
  const cartItems = cart[userId] || [];
  return cartItems;
};

const updateLocalStorageForCart = (productId) => {
  const userId = getUserId();
  const cart = JSON.parse(localStorage.getItem("cart")) || {};
  const userCart = cart[userId] || [];
  const productIndex = userCart.findIndex((item) => item.id === productId);
  if (productIndex !== -1) {
    userCart[productIndex].quantity += 1;
  } else {
    userCart.push({ id: productId, quantity: 1 });
  }
  cart[userId] = userCart;
  localStorage.setItem("cart", JSON.stringify(cart));
};

const getLocalStorageCartQuantity = () => {
  const userId = getUserId();
  const cart = JSON.parse(localStorage.getItem("cart")) || {};
  const userCart = cart[userId] || [];
  const totalQuantity = userCart.reduce((sum, item) => sum + item.quantity, 0);
  return totalQuantity;
};

const getAllProductIds = () => {
  const userId = getUserId();
  const cart = JSON.parse(localStorage.getItem("cart")) || {};
  const userCart = cart[userId] || [];
  const productIds = userCart.map((item) => parseInt(item.id));
  return productIds;
};

const cartIconQuantity = () => {
  const navCartQuantity = document.querySelector(".nav-side--link-quantity");
  if (navCartQuantity) {
    const totalQuantity = getLocalStorageCartQuantity();
    if (totalQuantity != 0) {
      navCartQuantity.textContent = totalQuantity;
    } else {
      navCartQuantity.textContent = "";
    }
  }
};

const addToCart = (e) => {
  const currentBtn = e.target;
  const productId = currentBtn.getAttribute("data-product-id");

  if (productId) {
    currentBtn.textContent = "Adding...";
    currentBtn.classList.add("disabled");
    updateLocalStorageForCart(productId);

    setTimeout(() => {
      currentBtn.textContent = "Added";
      Swal.fire({
        icon: "success",
        title: "Product has been added to cart!!",
        showConfirmButton: true,
      });
      cartIconQuantity();
      setTimeout(() => {
        currentBtn.textContent = "Add to Cart";
        currentBtn.classList.remove("disabled");
      }, 2000);
    }, 2000);
  } else {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Something went wrong! Please try again later...",
    });
  }
};

cartIconQuantity();

const onApplyGiftCardClick = async () => {
  const gitftCardCode = document.getElementById("giftCardCodeInput").value;
  // reset gift card detail
  if (!gitftCardCode) {
    const giftcardCreditEle = document.getElementById("giftcard-credit");
    const totalTopayEle = document.getElementById("total-to-pay");
    const previoursValue = totalTopayEle.getAttribute("persistent-totalTopay");
    totalTopayEle.textContent = `$ ${previoursValue}`;
    totalTopayEle.setAttribute("total-amount", previoursValue);
    //   clear the local-storage
    localStorage.removeItem("giftcardDetail");

    giftcardCreditEle.setAttribute("giftCardApplied", "");
    return;
  }

  if (gitftCardCode) {
    const rep = await fetch("/giftcard/validate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        gf_card_id: gitftCardCode,
      }),
    });
    if (rep.ok) {
      const data = await rep.json();
      // const giftcardCredit = data.amount;
      const { gf_card_id, amount, holder } = data;
      const giftcardCredit = Number(amount);
      const giftcardCreditEle = document.getElementById("giftcard-credit");
      const infoLabelEle = document.getElementById("giftcard-credit-label");

      localStorage.setItem("giftcardDetail", JSON.stringify(data));
      const giftCardApplied = giftcardCreditEle.getAttribute("giftCardApplied");
      if (giftCardApplied === gitftCardCode) {
        // avoid user repeatly apply same gift card code
        return;
      }

      giftcardCreditEle.textContent = Number(giftcardCredit).toFixed(2);
      giftcardCreditEle.setAttribute("data-gift-card", true);
      // avoid user repeatly apply same gift card code
      giftcardCreditEle.setAttribute("giftCardApplied", gitftCardCode);
      infoLabelEle.textContent = `Pay by Gift Card : ${gitftCardCode} - $${Number(
        giftcardCredit
      ).toFixed(2)}`;
      const totalTopayEle = document.getElementById("total-to-pay");
      if (totalTopayEle) {
        const value = totalTopayEle.getAttribute("total-amount");
        const total = Number(value);
        const residue = total - Number(giftcardCredit);
        if (residue >= 0) {
          totalTopayEle.textContent = `$${residue.toFixed(2)}`;
          totalTopayEle.setAttribute("total-amount", residue);
          //  show info to user : gift card has no remain
          giftcardCreditEle.textContent = `Your GiftCard remaining amount is: $0`;
        } else {
          giftcardCreditEle.textContent = `$${(-residue).toFixed(2)}`;
          totalTopayEle.textContent = `$0`;
          totalTopayEle.setAttribute("total-amount", 0);
        }
      }
    } else {
      giftcardCreditEle = document.getElementById("giftcard-credit");
      giftcardCreditEle.innerHTML = `<span style="color : red">You have no GiftCard with ID: ${gitftCardCode}</span>`;
      localStorage.removeItem("giftcardDetail");
    }
  }
};

const applyGiftCardBtn = document.getElementById("applyGiftCardBtn");
if (applyGiftCardBtn) {
  applyGiftCardBtn.addEventListener("click", onApplyGiftCardClick);
}

const getRenderAddress = () => {
  const userId = getUserId();
  fetch(`/checkout/get_user_address?user_id=${userId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      let addressContent = "";
      if (data && data.data && Object.keys(data.data).length != 0) {
        const address = data.data;
        addressContent = `
			<div>
			  ${address[0] ? `${address[0]} <br />` : ""}
			  ${address[1] ? `${address[1]} <br />` : ""}
			  ${address[2] ? `${address[2]} <br />` : ""}
			  ${address[3] ? `${address[3]} <br />` : ""}
			  ${address[4] ? `${address[4]}` : ""}
			</div>
		  `;
        document.getElementById("payButton").disabled = false;
      } else {
        addressContent = `
			<div>
			  You haven't set a default shipping address yet. 
			  Please go to <a href="/shipping/manage_addresses/${userId}">Address</a> page to set it up.
			</div>
		  `;
      }
      const shippingAddressEle = document.querySelector("#shipping-address");
      const shippingTypeSelect = document.getElementById(
        "shipping-type-select"
      );
      const shippingMethodEle = document.getElementById(
        "shipping-method-in-checkout-pop"
      );
      const selectedShippingType = shippingTypeSelect.value;
      // const shipping
      if (
        addressContent &&
        shippingAddressEle &&
        selectedShippingType !== "pickup"
      ) {
        shippingMethodEle.textContent = "Shipping To :";
        shippingAddressEle.innerHTML = addressContent;
      }
      if (selectedShippingType === "pickup") {
        shippingMethodEle.textContent = "Shipping Method :";
        shippingAddressEle.textContent = "Pick Up";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

// remove the existing credit card input box if gift card is enough to pay out
const checkPayWithGiftCard = () => {
  const totalTtoPayEle = document.getElementById("total-to-pay");
  if (totalTtoPayEle) {
    const totalAmount = Number(totalTtoPayEle.getAttribute("total-amount"));
    if (totalAmount == 0) {
      const nameOnCard = document.getElementById("NameOnCardBox");
      nameOnCard.parentNode.removeChild(nameOnCard);
      const cardNumberBox = document.getElementById("cardNumberBox");
      cardNumberBox.parentNode.removeChild(cardNumberBox);
      const ExpiryDateBox = document.getElementById("ExpiryDateBox");
      ExpiryDateBox.parentNode.removeChild(ExpiryDateBox);
      const CVVBox = document.getElementById("CVVBox");
      CVVBox.parentNode.removeChild(CVVBox);
    }
  }
};

//   function to pop up checkout window
const proceedCheckout = (flag) => {
  const checkoutPopup = document.querySelector(".checkout--container");
  if (checkoutPopup) {
    if (flag) {
      getRenderAddress();
      checkoutPopup.classList.add("active");
      checkPayWithGiftCard();
    } else {
      checkoutPopup.classList.remove("active");
    }
  }
};

//   function to handle cart chekout button click
const btnCartCheckout = document.querySelector("#cart-checkout-btn");
if (btnCartCheckout) {
  btnCartCheckout.addEventListener("click", (e) => {
    e.preventDefault();
    proceedCheckout(true);
  });
}

//   function to close pop up
const checkoutPopupOverlay = document.querySelector(".checkout--overlay");
if (checkoutPopupOverlay) {
  checkoutPopupOverlay.addEventListener("click", (e) => {
    e.preventDefault();
    proceedCheckout(false);
  });
}

const ctaAddToCart_btns = document.querySelectorAll(".cta-add-to-cart");
ctaAddToCart_btns.forEach((btn) => {
  btn.addEventListener("click", (event) => addToCart(event));
});

class CartTable extends HTMLElement {
  constructor() {
    super();
    this.checkCartQuantity();
    this.fetchProductsDetails();
  }
  toggleLoading(flag) {
    const loadingTarget = document.querySelector(
      ".cart--container .loading-container"
    );
    if (loadingTarget) {
      if (flag) {
        loadingTarget.classList.remove("displayNone");
      } else {
        loadingTarget.classList.add("displayNone");
      }
    }
  }
  checkCartQuantity() {
    const totalQuantity = getLocalStorageCartQuantity();
    const cartTableWithProducts = document.querySelector(
      ".cart--details.with-products"
    );
    const cartTableWithoutProducts = document.querySelector(
      ".cart--details.without-products"
    );
    if (totalQuantity > 0) {
      if (cartTableWithProducts)
        cartTableWithProducts.classList.remove("displayNone");
      if (cartTableWithoutProducts)
        cartTableWithoutProducts.classList.add("displayNone");
    } else {
      if (cartTableWithProducts)
        cartTableWithProducts.classList.add("displayNone");
      if (cartTableWithoutProducts)
        cartTableWithoutProducts.classList.remove("displayNone");
    }
  }
  fetchProductsDetails() {
    const allProductIds = getAllProductIds();
    if (allProductIds.length > 0) {
      fetch("/product/get_products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product_ids: allProductIds }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.updateLocalStorageProductPrices(data);
          this.renderCartProducts(data);
          this.updateOrderSummary(data);
        })
        .catch((error) => {
          console.error(
            "There has been a problem with your fetch operation:",
            error
          );
        });
    }
  }
  updateLocalStorageProductPrices(products) {
    const userId = getUserId();
    const cart = JSON.parse(localStorage.getItem("cart")) || {};
    const userCart = cart[userId] || [];

    products.forEach((product) => {
      const cartItem = userCart.find((item) => item.id == product.product_id);
      if (cartItem) {
        cartItem.price = parseFloat(product.price);
      }
    });

    cart[userId] = userCart;
    localStorage.setItem("cart", JSON.stringify(cart));
  }
  renderCartProducts(products) {
    const cartItems = getCartItems();

    let productHTML = "";
    products.forEach((product) => {
      const cartItem = cartItems.find((item) => item.id == product.product_id);
      const quantity = cartItem ? cartItem.quantity : 1;

      const productImagePath = `/static/images/products/${product.pd_image_path}`;

      productHTML += `
		  <div class="cart-product">
			<div class="cart-product--img">
			  <img src="${productImagePath}" alt="${product.name}">
			</div>
			<div class="cart-product--content">
			  <div class="cart-product--content-title">${product.name}</div>
			  <div class="cart-product--content-price">$${
          product.discounted_price
            ? "discounted: " + product.discounted_price
            : product.price
        }</div>
			  <div class="cart-product--content-quantity">
				<div class="cart-product--quantity">
				  <div class="cart-product--quantity-label">Qty.</div>
				  <div class="cart-product--quantity-selector">
					<input type="button" class="cart-product--quantity-control minus" value="-" data-current-product="${
            product.product_id
          }">
					<input type="text" class="cart-product--quantity-input" readonly value="${quantity}">
					<input type="button" class="cart-product--quantity-control plus" value="+" data-current-product="${
            product.product_id
          }">
				  </div>
				</div>
				<div class="cart-product--button">
				  <a href="#" class="cart-product--remove" data-current-product="${
            product.product_id
          }">
					<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon icon--cross" aria-label="Cross Icon">
					  <path d="m18 18-6.06-6m0 0L6 6.12M11.94 12 18 6m-6.06 6L6 17.88" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
					</svg>
				  </a>
				</div>
			  </div>
			</div>
		  </div>
		`;
    });

    const cartContainer = document.querySelector(
      ".cart--details.with-products .cart-left--container"
    );
    if (cartContainer) {
      cartContainer.innerHTML = "";
      cartContainer.innerHTML = productHTML;
      this.checkCartQuantity();
      this.bindQuantityChange();
    }
  }
  updateCartQuantity(productId, change) {
    const userId = getUserId();
    let cart = JSON.parse(localStorage.getItem("cart")) || {};
    const cartItems = cart[userId] || [];
    const productIndex = cartItems.findIndex((item) => item.id == productId);

    if (productIndex !== -1) {
      cartItems[productIndex].quantity += change;

      if (cartItems[productIndex].quantity <= 0) {
        cartItems.splice(productIndex, 1);
      }

      localStorage.setItem("cart", JSON.stringify(cart));
      cartIconQuantity();
      this.fetchProductsDetails();
      this.toggleLoading(false);
    }
  }
  removeProductFromCart(productId) {
    const userId = getUserId();
    let cart = JSON.parse(localStorage.getItem("cart")) || {};
    const cartItems = cart[userId] || [];
    const productIndex = cartItems.findIndex((item) => item.id == productId);

    if (productIndex !== -1) {
      cartItems.splice(productIndex, 1);
      localStorage.setItem("cart", JSON.stringify(cart));
      cartIconQuantity();
      this.fetchProductsDetails();
      this.toggleLoading(false);
      if (cartItems.length == 0) {
        const cartTableWithProducts = document.querySelector(
          ".cart--details.with-products"
        );
        const cartTableWithoutProducts = document.querySelector(
          ".cart--details.without-products"
        );
        if (cartTableWithProducts)
          cartTableWithProducts.classList.add("displayNone");
        if (cartTableWithoutProducts)
          cartTableWithoutProducts.classList.remove("displayNone");
      }
    }
  }
  bindQuantityChange() {
    const quantityControls = document.querySelectorAll(
      ".cart--container .cart-product--quantity-control"
    );
    if (quantityControls) {
      quantityControls.forEach((control) => {
        control.addEventListener("click", () => {
          this.toggleLoading(true);
          const productId = control.dataset.currentProduct;
          let change = 1;
          if (control.classList.contains("minus")) {
            change = -1;
          }
          setTimeout(() => {
            this.updateCartQuantity(productId, change);
          }, 1000);
        });
      });
    }

    const itemRemoveControls = document.querySelectorAll(
      ".cart--container .cart-product--remove"
    );
    if (itemRemoveControls) {
      itemRemoveControls.forEach((control) => {
        control.addEventListener("click", (e) => {
          e.preventDefault();
          this.toggleLoading(true);
          const productId = control.dataset.currentProduct;
          setTimeout(() => {
            this.removeProductFromCart(productId);
          }, 1000);
        });
      });
    }
  }
  updateOrderSummary(products) {
    const cartItems = getCartItems();

    let totalPrice = 0;
    let hasOversizedItem = false;

    products.forEach((product) => {
      const cartItem = cartItems.find((item) => item.id == product.product_id);
      const quantity = cartItem ? cartItem.quantity : 1;
      let product_price = product.discounted_price
        ? product.discounted_price
        : product.price;
      totalPrice += product_price * quantity;
      if (product.shipping_type === "oversized") {
        hasOversizedItem = true;
      }
    });

    const cart_table = document.querySelector("#cart-table");

    const orderSummaryTotal = document.querySelector("#order-summary-total");
    if (orderSummaryTotal) {
      orderSummaryTotal.textContent = `$${totalPrice.toFixed(2)}`;
      cart_table.setAttribute("data-total", totalPrice);
    }

    const orderSummaryGST = document.querySelector("#order-summary-gst");
    if (orderSummaryGST) {
      const totalGST = totalPrice * 0.15;
      orderSummaryGST.textContent = `$${totalGST.toFixed(2)}`;
      cart_table.setAttribute("data-gst", totalGST);
    }

    const shippingTypeSelect = document.getElementById("shipping-type-select");
    const orderSummaryShipping = document.getElementById(
      "order-summary-shipping"
    );

    const standardPrice = parseFloat(
      shippingTypeSelect.querySelector("option[value='standard']").dataset.price
    );
    const oversizedPrice = parseFloat(
      shippingTypeSelect.querySelector("option[value='oversized']").dataset
        .price
    );
    const pickupPrice = parseFloat(
      shippingTypeSelect.querySelector("option[value='pickup']").dataset.price
    );

    if (hasOversizedItem) {
      shippingTypeSelect.innerHTML = `
		  <option value="oversized" data-price="${oversizedPrice}">Oversized - $${oversizedPrice.toFixed(
        2
      )}</option>
		  <option value="pickup" data-price="${pickupPrice}">Pickup - $${pickupPrice.toFixed(
        2
      )}</option>
		`;
      if (orderSummaryShipping) {
        orderSummaryShipping.textContent = `$${oversizedPrice.toFixed(2)}`;
        cart_table.setAttribute("data-freight", oversizedPrice);
      }
    } else {
      shippingTypeSelect.innerHTML = `
		  <option value="standard" data-price="${standardPrice}">Standard - $${standardPrice.toFixed(
        2
      )}</option>
		  <option value="pickup" data-price="${pickupPrice}">Pickup - $${pickupPrice.toFixed(
        2
      )}</option>
		`;
      if (orderSummaryShipping) {
        orderSummaryShipping.textContent = `$${standardPrice.toFixed(2)}`;
        cart_table.setAttribute("data-freight", standardPrice);
      }
    }

    const totalTopay = document.getElementById("total-to-pay");
    if (
      orderSummaryTotal &&
      orderSummaryGST &&
      orderSummaryShipping &&
      totalTopay
    ) {
      const total =
        Number(cart_table.getAttribute("data-gst")) +
        Number(cart_table.getAttribute("data-total")) +
        Number(cart_table.getAttribute("data-freight"));
      totalTopay.textContent = `$${total.toFixed(2)}`;
      totalTopay.setAttribute("total-amount", total);
      totalTopay.setAttribute("persistent-totalTopay", total);
    }
  }
}

customElements.define("cart-table", CartTable);

const updateShippingCost = () => {
  var shippingCost = 0;
  const shippingTypeSelect = document.getElementById("shipping-type-select");
  if (shippingTypeSelect && shippingTypeSelect.value) {
    const selectedShippingType = shippingTypeSelect
      ? shippingTypeSelect.value
      : "None";
    const selectedOption =
      shippingTypeSelect.options[shippingTypeSelect.selectedIndex];
    shippingCost = parseFloat(selectedOption.dataset.price);
  }

  const cartTable = document.querySelector("#cart-table");
  const orderSummaryShipping = document.getElementById(
    "order-summary-shipping"
  );

  if (orderSummaryShipping) {
    orderSummaryShipping.textContent = `$${shippingCost.toFixed(2)}`;
  }
  if (cartTable) {
    cartTable.setAttribute("data-freight", shippingCost);
    const totalGST = parseFloat(cartTable.getAttribute("data-gst"));
    const total = parseFloat(cartTable.getAttribute("data-total"));
    const totalToPay = total + totalGST + shippingCost;
    const totalTopayEle = document.getElementById("total-to-pay");
    totalTopayEle.textContent = `$${totalToPay.toFixed(2)}`;
    totalTopayEle.setAttribute("total-amount", `$${totalToPay.toFixed(2)}`);
    totalTopayEle.setAttribute(
      "persistent-totalTopay",
      `${totalToPay.toFixed(2)}`
    );

    const orderSummaryTotal = document.getElementById("order-summary-total");
    if (orderSummaryTotal) {
      orderSummaryTotal.textContent = `$${total.toFixed(2)}`;
    }

    const orderSummaryGST = document.getElementById("order-summary-gst");
    if (orderSummaryGST) {
      orderSummaryGST.textContent = `$${totalGST.toFixed(2)}`;
    }
  }
};

document.addEventListener("DOMContentLoaded", () => {
  updateShippingCost();
});

class CheckoutPop extends HTMLElement {
  constructor() {
    super();
    this.limitExpireDateInput();
    this.limitCardNumber();
    this.limitCVV();
    this.paymentSubmit();
  }

  limitExpireDateInput() {
    const expiryInput = document.getElementById("expiryDate");

    expiryInput.addEventListener("input", (event) => {
      const currentTarget = event.target;
      let value = currentTarget.value;
      let formatExpireValue = value.replace(/\D/g, "");
      if (formatExpireValue.length > 4) {
        formatExpireValue = formatExpireValue.slice(0, 4);
      }
      formatExpireValue = formatExpireValue.replace(/(\d{2})(?=\d{2})/g, "$1/");
      currentTarget.value = formatExpireValue.trim();
    });
  }
  limitCardNumber() {
    const cardNumberInput = document.getElementById("cardNumber");

    cardNumberInput.addEventListener("input", (event) => {
      const currentTarget = event.target;
      let value = currentTarget.value;
      let formatCardNumber = value.replace(/\D/g, "");
      if (formatCardNumber.length > 16) {
        formatCardNumber = formatCardNumber.slice(0, 16);
      }
      currentTarget.value = formatCardNumber.trim();
    });
  }
  limitCVV() {
    const cvvInput = document.getElementById("cvv");

    cvvInput.addEventListener("input", (event) => {
      const currentTarget = event.target;
      let value = currentTarget.value;
      let formatCVVValue = value.replace(/\D/g, "");
      if (formatCVVValue.length > 3) {
        formatCVVValue = formatCVVValue.slice(0, 3);
      }
      currentTarget.value = formatCVVValue.trim();
    });
  }
  validateName(name) {
    return name.trim() !== "";
  }
  validateCardNumber(cardNumber) {
    const regex = /^\d{16}$/;
    return regex.test(cardNumber);
  }
  validateExpiryDate(expiryDate) {
    const regex = /^(0[1-9]|1[0-2])\/\d{2}$/;
    if (!regex.test(expiryDate)) {
      return false;
    }

    const today = new Date();
    const currentMonth = today.getMonth() + 1;
    const currentYear = today.getFullYear().toString().slice(-2);

    const [expMonth, expYear] = expiryDate.split("/");
    if (parseInt(expYear) < parseInt(currentYear)) {
      return false;
    }
    if (
      parseInt(expYear) === parseInt(currentYear) &&
      parseInt(expMonth) < currentMonth
    ) {
      return false;
    }

    return true;
  }
  validateCVV(cvv) {
    const regex = /^\d{3,4}$/;
    return regex.test(cvv);
  }

  paymentSubmit() {
    document
      .getElementById("payment-form")
      .addEventListener("submit", (event) => {
        event.preventDefault();
        const cart_table = document.querySelector("#cart-table");
        const { userId, total, gst, freight } = cart_table.dataset;
        const giftcardCreditEle = document.getElementById("giftcard-credit");
        const giftCardId = giftcardCreditEle.getAttribute("giftCardApplied");
      
	const useGiftCard = localStorage.getItem("giftcardDetail")
        if (
          document.getElementById("name") &&
          document.getElementById("cardNumber") &&
          document.getElementById("cvv")
        ) {
          const name = document.getElementById("name").value;
          const cardNumber = document.getElementById("cardNumber").value;
          const expiryDate = document.getElementById("expiryDate").value;
          const cvv = document.getElementById("cvv").value;
          var isValid = true;
          document.getElementById("nameError").textContent = "";
          document.getElementById("cardNumberError").textContent = "";
          document.getElementById("expiryDateError").textContent = "";
          document.getElementById("cvvError").textContent = "";

          if (!this.validateName(name)) {
            document.getElementById("nameError").textContent =
              "* Please enter your name on the card.";
            isValid = false;
          }
          if (!this.validateCardNumber(cardNumber)) {
            document.getElementById("cardNumberError").textContent =
              "* Please enter a valid 16-digit card number.";
            isValid = false;
          }
          if (!this.validateExpiryDate(expiryDate)) {
            document.getElementById("expiryDateError").textContent =
              "* Please enter a valid expiry date (MM/YY).";
            isValid = false;
          }
          if (!this.validateCVV(cvv)) {
            document.getElementById("cvvError").textContent =
              "* Please enter a valid 3 or 4-digit CVV.";
            isValid = false;
          }
          if (isValid) {
            document.getElementById("payButton").disabled = true;
            document.getElementById("message").textContent =
              "Processing your payment...";

            this.proceedPayment(
              userId,
              total,
              useGiftCard ? "gift-card" : "Credit Card",
              gst,
              freight,
              giftCardId
            );
          }
        } else {
          document.getElementById("payButton").disabled = true;
          document.getElementById("message").textContent =
            "Processing your payment...";
          this.proceedPayment(
            userId,
            total,
            "gift-card",
            gst,
            freight,
            giftCardId
          );
        }
      });
  }

  proceedPayment(userId, total, paymentType, gst, freight, giftCardId) {
    const cart = JSON.parse(localStorage.getItem("cart")) || {};
    const cartItems = cart[userId] || [];

    const data = {
      userId,
      total,
      paymentType,
      gst,
      freight,
      cartItems,
      giftCardId,
    };

    fetch("/checkout/proceed_payment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        const checkoutPopup = document.querySelector(".checkout--container");
        checkoutPopup.classList.remove("active");
        Swal.fire({
          icon: "success",
          title: "Payment made successfully!",
          html: `Now, you can check your order from your <a href="/login">dashboard</a>!`,
          showConfirmButton: true,
        });
        delete cart[userId];
        localStorage.setItem("cart", JSON.stringify(cart));
        const cartTableWithProducts = document.querySelector(
          ".cart--details.with-products"
        );
        const cartTableWithoutProducts = document.querySelector(
          ".cart--details.without-products"
        );
        if (cartTableWithProducts)
          cartTableWithProducts.classList.add("displayNone");
        if (cartTableWithoutProducts)
          cartTableWithoutProducts.classList.remove("displayNone");
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

customElements.define("checkout-pop", CheckoutPop);
