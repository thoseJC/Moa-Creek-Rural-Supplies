class InventoryManagement extends HTMLElement {
  constructor() {
    super();
    this._this = this;
    this.bindClick();
    // this.applyCreditApprove();
  }
  bindClick() {
    const targetElement = this.querySelector('.inventory--container');
    const manageInventoryBtns = document.querySelectorAll('.cta-manage-inventory');
    if (targetElement) {
      manageInventoryBtns.forEach(btn => {
        btn.addEventListener('click', event => {
          event.preventDefault();
          targetElement.classList.add('active');
          const currentEle = event.currentTarget;
          const {
            inventoryId,
            productId
          } = currentEle.dataset;
          console.log('inventoryId', inventoryId);
          console.log('productId', productId);
          this.getProductDetails(productId)
        })
      })

      const inventoryPopOverlay = this.querySelector('.inventory--overlay');
      if (inventoryPopOverlay) {
        inventoryPopOverlay.addEventListener('click', () => {
          targetElement.classList.remove('active');
          const contentSection = this.querySelector('.inventory-popup--section');
          if (contentSection) contentSection.classList.add('init');
          
          const loadingSection = this.querySelector('.loading-container');
          if (loadingSection) loadingSection.classList.remove('displayNone');
        })
      }
    }

    const inventoryUpdateBtn = this.querySelector('#submit-inventory-update');
    if (inventoryUpdateBtn) {
      inventoryUpdateBtn.addEventListener('click', event => {
        event.preventDefault();
        this.inventoryUpdate();
      })
    }
  }
  getProductDetails(product_id) {
    // const data = { product_id };
    fetch(`/staff/product_with_inventory?product_id=${product_id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('data', data);
      this.renderContent(data);
      // Swal.fire({
      //   icon: "success",
      //   title: "Credit Limit Increasement Application Approved!",
      //   html: `The customer will receive the noficiation on the dashboard now!`,
      //   showConfirmButton: true
      // }).then((result) => {
      //   if (result.isConfirmed) {
      //     window.location.href = '/manager/credit_management';
      //   }
      // });
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
    });
  }
  renderContent(product) {
    console.log('product', product);
    const productImg = this.querySelector('#inventory-product-img');
    if (productImg) productImg.src = `/static/images/products/${product.product_image}`;

    const productName = this.querySelector('#inventory-product-name');
    if (productName) productName.innerHTML = product.product_name;

    const productDes = this.querySelector('#inventory-product-description');
    if (productDes) productDes.innerHTML = product.product_description;

    const productPrice = this.querySelector('#inventory-unit-price');
    if (productPrice) productPrice.innerHTML = `$${product.product_price}`;

    const productStatus = this.querySelector('#inventory-product-status');
    if (productStatus) productStatus.innerHTML = product.product_status == 1 ? 'Active' : 'Inactive';

    const productInventory = this.querySelector('#inventory-product-inventory');
    if (productInventory) productInventory.innerHTML = product.product_inventory;

    const additionalInventory = this.querySelector('#additional-inventory');
    if (additionalInventory) {
      additionalInventory.setAttribute('data-inventory-id', product.product_inventory_id);
      additionalInventory.setAttribute('data-current-inventory', product.product_inventory);
    }


    const contentSection = this.querySelector('.inventory-popup--section');
    if (contentSection) contentSection.classList.remove('init');
    
    const loadingSection = this.querySelector('.loading-container');
    if (loadingSection) loadingSection.classList.add('displayNone');
  }
  inventoryUpdate() {
    const additionalInventory = this.querySelector('#additional-inventory');
    let additionalInventoryValue = 0;
    let currentInventory = 0;
    let inventoryId;
    if (additionalInventory) {
      additionalInventoryValue = parseInt(additionalInventory.value);
      inventoryId = additionalInventory.dataset.inventoryId;
      currentInventory = parseInt(additionalInventory.dataset.currentInventory);
    }
    
    if (additionalInventoryValue != 0) {
      const newInventoryValue = currentInventory + additionalInventoryValue;

      console.log('additionalInventoryValue', additionalInventoryValue);
      console.log('inventoryId', inventoryId);
      console.log('newInventoryValue', newInventoryValue);
    }
  }
  applyCreditApprove() {
    const ctaCreditApply = this.querySelector('#cta-credit-apply');
    if (ctaCreditApply) {
      ctaCreditApply.addEventListener('click', event => {
        event.preventDefault();
        const loadingTarget = this.querySelector('.loading-container');
        if (loadingTarget) loadingTarget.classList.remove('displayNone');

        const popupCustomerCurrentLimit = this.querySelector('#customer-current-credit-limit');
        const creditLimit = popupCustomerCurrentLimit.getAttribute('data-current-limit');
        const popupInputApplyCredit = this.querySelector('#input-for-apply-credit');
        const creditApply = popupInputApplyCredit.value;

        const data = {
          user_id: this.userId,
          credit_limit: creditLimit,
          credit_remaining: this.creditRemaining,
          credit_apply: creditApply
        }

        fetch('/manager/update_credit_apply', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          Swal.fire({
            icon: "success",
            title: "Credit Limit Increasement Application Approved!",
            html: `The customer will receive the noficiation on the dashboard now!`,
            showConfirmButton: true
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.href = '/manager/credit_management';
            }
          });
        })
        .catch(error => {
          console.error('There has been a problem with your fetch operation:', error);
        });
      })
    }
  }
}

customElements.define('inventory-management', InventoryManagement);