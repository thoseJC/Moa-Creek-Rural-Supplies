  class CategoryCards extends HTMLElement {
    constructor() {
      super();

      this.sliderFunc();
    }
    sliderFunc() {
      const categoryCardsContainer = this.querySelector('#home-category-cards');
      const categoryCards = this.querySelectorAll('.category-card');

      if (categoryCards.length > 3 && categoryCardsContainer) {
        const flkty = new Flickity(categoryCardsContainer, {
          cellAlign: 'left',
          wrapAround: true,
          contain: true,
          pageDots: false
        });
      }
    }
  }

  customElements.define('category-cards', CategoryCards);

class ProductCards extends HTMLElement {
  constructor() {
    super();

    this.sliderFunc();
  }
  sliderFunc() {
    const productCardsContainer = this.querySelector('.product-cards');
    const productCards = this.querySelectorAll('.product-card');

    if (productCards.length > 4) {
      const flkty = new Flickity(productCardsContainer, {
        cellAlign: 'left',
        wrapAround: true,
        contain: true,
        pageDots: false
      });
    }
  }
}

customElements.define('product-cards', ProductCards);