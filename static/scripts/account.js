class CreditPop extends HTMLElement {
  constructor() {
    super();
    this.bindClick();
    this.draggableLine();
    this.applyIncreasingCredit();
  }
  bindClick() {
    const creditPopCTA = document.querySelector('#cta-credit-pop');
    if (creditPopCTA) {
      creditPopCTA.addEventListener('click', () => {
        this.classList.add('active')
      })
    }

    const creditPopOverlay = this.querySelector('.credit--overlay');
    if (creditPopOverlay) {
      creditPopOverlay.addEventListener('click', () => {
        this.classList.remove('active')
      })
    }
  }
  draggableLine() {
    const compareCurrentNewValues = () => {
      const targetElement = document.querySelector('#rangeValue');
      const applyIncreasingCreditBtn = document.querySelector('#cta-apply-credit');
      if (targetElement) {
        const currentLimit = parseFloat(targetElement.dataset.currentLimit);
        const newLimit = parseFloat(targetElement.dataset.newLimit);
        if (currentLimit == newLimit) {
          applyIncreasingCreditBtn.classList.add('disabled');
        } else {
          applyIncreasingCreditBtn.classList.remove('disabled');
        }
      }
    }
    const rangeSlider = event => {
      compareCurrentNewValues();
      const newValue = event.target.value;
      const targetElement = document.querySelector('#rangeValue');
      if (targetElement) {
        targetElement.innerHTML = newValue;
        targetElement.setAttribute('data-new-limit', newValue);
      }
    }
    const line = document.querySelector('#credit-range');
    if (line) {
      line.addEventListener('change', event => {
        rangeSlider(event);
      })
      line.addEventListener('mousemove', event => {
        rangeSlider(event);
      })
    }
  }
  applyIncreasingCredit() {
    const applyIncreasingCreditBtn = document.querySelector('#cta-apply-credit');
    if (applyIncreasingCreditBtn) {
      applyIncreasingCreditBtn.addEventListener('click', event => {
        if (applyIncreasingCreditBtn.classList.contains('disabled')) return;
        event.preventDefault();
        const parentElement = document.querySelector('.credit--container');
        const loadingTarget = parentElement.querySelector('.loading-container');
        if (loadingTarget) {
          loadingTarget.classList.remove('displayNone');
        }

        const targetElement = document.querySelector('#rangeValue');
        if (targetElement) {
          const new_limit = parseFloat(targetElement.dataset.newLimit);
          const data = {
            new_limit
          }

          setTimeout(() => {
            fetch('/customer/credit_apply', {
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
                title: "Credit Limit Increasement Application submitted successfully!",
                html: `The administrator will review your application ang get back to you soon!`,
                showConfirmButton: true
              }).then((result) => {
                if (result.isConfirmed) {
                  window.location.href = '/customer/credit';
                }
              });
            })
            .catch((error) => {
              console.error('Error:', error);
            })
            .finally(() => {
              if (parentElement) parentElement.classList.remove('active');
            })
          }, 2000);
        }

      })
    }
  }
}

customElements.define('credit-pop', CreditPop);


class OrdersList extends HTMLElement {
  constructor() {
    super();
    this.bindClick();
    this.download();
  }
  bindClick() {
    const viewOrdersBtns = document.querySelectorAll('.cta-view-order-details');
    const orderPopup = document.querySelector('.order--container');
    viewOrdersBtns.forEach(btn => {
      btn.addEventListener('click', event => {
        event.preventDefault();
        const currentTarget = event.currentTarget;
        if (orderPopup) orderPopup.classList.add('active');
        this.getOrderDetails(currentTarget.dataset.orderId);
      })
    })

    const orderPopOverlay = document.querySelector('.order--overlay');
    if (orderPopOverlay) {
      orderPopOverlay.addEventListener('click', () => {
        if (orderPopup) orderPopup.classList.remove('active');
      })
    }
  }
  getOrderDetails(orderId) {
    const data = {
      order_id: orderId
    }

    fetch('/customer/order_details', {
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
      this.renderOrderDetails(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    })
  }
  renderOrderDetails(data) {
    let orderBody = '';
    let orderId = '';
    let orderDate = '';
    let orderStatus = '';
    let addressCustomer = '';
    let addressStreet = '';
    let addressState = '';
    let addressCity = '';
    let addressPostcode = '';
    let addressCountry = '';
    let orderGst = 0;
    let orderTotal = 0;
    let orderShipping = 0;


    if (data.length) {
      orderId = data[0][0];
      orderDate = data[0][1];
      orderStatus = data[0][3];
      addressCustomer = `${data[0][4]} ${data[0][5]}`;
      addressStreet = data[0][6];
      addressState = data[0][7];
      addressCity = data[0][8];
      addressPostcode = data[0][9];
      addressCountry = data[0][10];
      orderGst = data[0][15];
      // orderTotal = data[0][2];
      orderShipping = data[0][16];


      const products = data.map(item => ({
        productName: item[11],
        productImage: item[12],
        productUnitPrice: parseFloat(item[13]),
        productQuantity: item[14]
      }));

      products.forEach(product => {
        const totalPrice = product.productUnitPrice * product.productQuantity;
        orderTotal += totalPrice;
        orderBody += `
          <tr>
            <td class="order-product">
              <div class="order-product--wrapper">
                <div class="order-product--img">
                  <img src="/static/images/products/${product.productImage}" alt="${product.productName}" />
                </div>
                <div class="order-product--name">${product.productName}</div>
              </div>
            </td>
            <td class="order-item">
              <div class="order-item--value">$${product.productUnitPrice.toFixed(2)}</div>
            </td>
            <td class="order-item">
              <div class="order-item--value">${product.productQuantity}</div>
            </td>
            <td class="order-item">
              <div class="order-item--value">$${totalPrice.toFixed(2)}</div>
            </td>
          </tr>
        `;
      });
    }
    const updateElementText = (selector, text) => {
      const element = document.querySelector(selector);
      if (element) element.innerHTML = text;
    };
  
    updateElementText('#order-list tbody', orderBody);
    updateElementText('#order-id', orderId);
    updateElementText('#order-date', orderDate);
    updateElementText('#order-status', orderStatus);
    updateElementText('#address-customer', addressCustomer);
    updateElementText('#address-street', addressStreet);
    updateElementText('#address-state', addressState);
    updateElementText('#address-city', addressCity);
    updateElementText('#address-postcode', addressPostcode);
    updateElementText('#address-country', addressCountry);
    updateElementText('#order-gst', `$${orderGst ? orderGst : orderGst.toFixed(2)}`);
    updateElementText('#order-shipping', `$${orderShipping ? orderShipping : orderShipping.toFixed(2)}`);
    updateElementText('#order-total', `$${orderTotal.toFixed(2)}`);

    const targetEle = document.querySelector('#cta-download-receipt');
    if (targetEle) targetEle.setAttribute('data-order-id', orderId)
  }
  download() {
    const downloadBtn = document.querySelector('#cta-download-receipt');
    if (downloadBtn) {
      downloadBtn.addEventListener('click', async(event) => {
        event.preventDefault();
        const orderId = event.target.dataset.orderId;
        
        const { jsPDF } = window.jspdf;
        const element = document.getElementById('content-to-download');
        if (!element) {
            console.error('Element not found:', 'content-to-download');
            return;
        }
        const canvas = await html2canvas(element, {
          scale: 2,
          useCORS: true
        });
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'pt', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save(`receipt-${orderId}.pdf`);
      })
    }
  }
}

customElements.define('orders-list', OrdersList);