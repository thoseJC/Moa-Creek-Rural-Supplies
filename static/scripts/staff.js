class InventoryManagement extends HTMLElement {
  constructor() {
    super();
    this.bindClick();
    this.inventoryUpdate();
    this.newInventoryCheck();
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
  }
  getProductDetails(product_id) {
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
      this.renderContent(data);
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
    });
  }
  renderContent(product) {
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
    const inventoryUpdateBtn = this.querySelector('#submit-inventory-update');
    if (inventoryUpdateBtn) {
      inventoryUpdateBtn.addEventListener('click', event => {
        event.preventDefault();
        const loadingEle = this.querySelector('.loading-container');
        if (loadingEle) loadingEle.classList.remove('displayNone');

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
    
          const data = {
            inventory_id: inventoryId,
            new_inventory: newInventoryValue
          }
    
          fetch('/staff/update_product_inventory', {
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
            if (loadingEle) loadingEle.classList.add('displayNone');
            Swal.fire({
              icon: "success",
              title: "Inventory Updated Successfully!",
              showConfirmButton: true
            }).then((result) => {
              if (result.isConfirmed) {
                window.location.href = '/staff/inventory_management';
              }
            });
          })
          .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
          });
        }
      })
    }
  }
  newInventoryCheck() {
    const inventoryInput = this.querySelector('#additional-inventory');
    const submitBtn = this.querySelector('#submit-inventory-update');
    if (inventoryInput && submitBtn) {
      inventoryInput.addEventListener('change', event => {
        const newValue = parseInt(event.currentTarget.value);
        if (newValue > 0) {
          submitBtn.classList.remove('disabled');
        } else {
          submitBtn.classList.add('disabled');
        }
      })
    }
  }
}

customElements.define('inventory-management', InventoryManagement);