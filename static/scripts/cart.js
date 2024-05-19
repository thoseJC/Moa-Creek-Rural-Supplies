const getUserId = () => {
  let userId = 0;
  const navCartQuantity = document.querySelector('.nav-side--link-quantity');
  if (navCartQuantity.dataset.userId) userId = navCartQuantity.dataset.userId;
  return userId;
}

const getCartItems = () => {
  const userId = getUserId();
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const cartItems = cart[userId] || [];
  return cartItems;
}

const updateLocalStorageForCart = (productId) => {
  const userId = getUserId();
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const userCart = cart[userId] || [];
  const productIndex = userCart.findIndex(item => item.id === productId);
  if (productIndex !== -1) {
    userCart[productIndex].quantity += 1;
  } else {
    userCart.push({ id: productId, quantity: 1 });
  }
  cart[userId] = userCart;
  localStorage.setItem('cart', JSON.stringify(cart));
}

const getLocalStorageCartQuantity = () => {
  const userId = getUserId();
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const userCart = cart[userId] || [];
  const totalQuantity = userCart.reduce((sum, item) => sum + item.quantity, 0);
  return totalQuantity;
}

const getAllProductIds = () => {
  const userId = getUserId();
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const userCart = cart[userId] || [];
  const productIds = userCart.map(item => parseInt(item.id));
  return productIds;
}

const cartIconQuantity = () => {
  const navCartQuantity = document.querySelector('.nav-side--link-quantity');
  if (navCartQuantity) {
    const totalQuantity = getLocalStorageCartQuantity();
    if (totalQuantity != 0) navCartQuantity.textContent = totalQuantity;
  }
}

const addToCart = e => {
  const currentBtn = e.target;
  const productId = currentBtn.getAttribute('data-product-id');

  if (productId) {
    currentBtn.textContent = 'Adding...';
    currentBtn.classList.add('disabled');
    updateLocalStorageForCart(productId);

    setTimeout(() => {
      currentBtn.textContent = 'Added';
      Swal.fire({
        icon: "success",
        title: "Product has been added to cart!!",
        showConfirmButton: true
      });
      cartIconQuantity();
      setTimeout(() => {
        currentBtn.textContent = 'Add to Cart';
        currentBtn.classList.remove('disabled');
      }, 2000);
    }, 2000);
  } else {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Something went wrong! Please try again later..."
    });
  }
}

cartIconQuantity();

const ctaAddToCart_btns = document.querySelectorAll('.cta-add-to-cart');
ctaAddToCart_btns.forEach(btn => {
  btn.addEventListener('click', event => addToCart(event));
});

class CartTable extends HTMLElement {
  constructor() {
    super();
    this.checkCartQuantity();
    this.fetchProductsDetails();
  }
  toggleLoading(flag) {
    const loadingTarget = document.querySelector('.cart--container .loading-container');
    if (loadingTarget) {
      if (flag) {
        loadingTarget.classList.remove('displayNone');
      } else {
        loadingTarget.classList.add('displayNone');
      }
    }
  }
  checkCartQuantity() {
    const totalQuantity = getLocalStorageCartQuantity();
    const cartTableWithProducts = document.querySelector('.cart--details.with-products');
    const cartTableWithoutProducts = document.querySelector('.cart--details.without-products');
    if (totalQuantity > 0) {
      if (cartTableWithProducts) cartTableWithProducts.classList.remove('displayNone');
    } else {
      if (cartTableWithoutProducts) cartTableWithoutProducts.classList.remove('displayNone');
    }
  }
  fetchProductsDetails() {
    const allProductIds = getAllProductIds();
    if (allProductIds) {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/get_products");
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

      xhr.onload = () => {
        if (xhr.status === 200) {
          var productsData = JSON.parse(xhr.responseText);
          this.renderCartProducts(productsData);
          this.updateOrderSummary(productsData)
        } else {
          console.error("Error getting products:", xhr.statusText);
        }
      };

      xhr.send(JSON.stringify({ "product_ids": allProductIds }));
    }
  }
  renderCartProducts(products) {
    const cartItems = getCartItems();

    let productHTML = '';
    products.forEach(product => {
      const cartItem = cartItems.find(item => item.id == product.product_id);
      const quantity = cartItem ? cartItem.quantity : 1;

      const productImagePath = `/static/images/products/${product.pd_image_path}`;

      productHTML += `
        <div class="cart-product">
          <div class="cart-product--img">
            <img src="${productImagePath}" alt="${product.name}">
          </div>
          <div class="cart-product--content">
            <div class="cart-product--content-title">${product.name}</div>
            <div class="cart-product--content-price">$${product.price}</div>
            <div class="cart-product--content-quantity">
              <div class="cart-product--quantity">
                <div class="cart-product--quantity-label">Qty.</div>
                <div class="cart-product--quantity-selector">
                  <input type="button" class="cart-product--quantity-control minus" value="-" data-current-product="${product.product_id}">
                  <input type="text" class="cart-product--quantity-input" readonly value="${quantity}">
                  <input type="button" class="cart-product--quantity-control plus" value="+" data-current-product="${product.product_id}">
                </div>
              </div>
              <div class="cart-product--button">
                <a href="#" class="cart-product--remove" data-current-product="${product.product_id}">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon icon--cross" aria-label="Cross Icon">
                    <path d="m18 18-6.06-6m0 0L6 6.12M11.94 12 18 6m-6.06 6L6 17.88" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      `;
    })

    const cartContainer = document.querySelector('.cart--details.with-products .cart-left--container');
    if (cartContainer) {
      cartContainer.innerHTML = '';
      cartContainer.innerHTML = productHTML;
      this.bindQuantityChange();
    }
  }
  updateCartQuantity(productId, change) {
    const cartItems = getCartItems();
    const productIndex = cartItems.findIndex(item => item.id == productId);
    
    if (productIndex !== -1) {
      cartItems[productIndex].quantity += change;
      
      if (cartItems[productIndex].quantity <= 0) {
        cartItems.splice(productIndex, 1);
      }
      
      localStorage.setItem('cart', JSON.stringify(cart));
      cartIconQuantity();
      this.fetchProductsDetails();
      this.toggleLoading(false);
    }
  }
  removeProductFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const productIndex = cart.findIndex(item => item.id == productId);
    
    if (productIndex !== -1) {
      cart.splice(productIndex, 1);
      localStorage.setItem('cart', JSON.stringify(cart));
      
      this.fetchProductsDetails();
      this.toggleLoading(false);
    }
  }
  bindQuantityChange() {
    const quantityControls = document.querySelectorAll('.cart--container .cart-product--quantity-control');
    if (quantityControls) {
      quantityControls.forEach(control => {
        control.addEventListener('click', () => {
          this.toggleLoading(true);
          const productId = control.dataset.currentProduct;
          let change = 1;
          if (control.classList.contains('minus')) {
            change = -1;
          }
          setTimeout(() => {
            this.updateCartQuantity(productId, change);
          }, 1000);
        })
      })
    }

    const itemRemoveControls = document.querySelectorAll('.cart--container .cart-product--remove');
    if (itemRemoveControls) {
      itemRemoveControls.forEach(control => {
        control.addEventListener('click', e => {
          e.preventDefault();
          this.toggleLoading(true);
          const productId = control.dataset.currentProduct;
          setTimeout(() => {
            this.removeProductFromCart(productId);
          }, 1000);
        })
      })
    }
  }
  updateOrderSummary(products) {
    const cartItems = getCartItems();

    let totalPrice = 0;

    products.forEach(product => {
      const cartItem = cartItems.find(item => item.id == product.product_id);
      const quantity = cartItem ? cartItem.quantity : 1;
      totalPrice += product.price * quantity;
    });

    const orderSummaryTotal = document.querySelector('#order-summary-total');
    if (orderSummaryTotal) {
      orderSummaryTotal.textContent = `$${totalPrice.toFixed(2)}`;
    }
  }
}

customElements.define('cart-table', CartTable);