class Card extends HTMLElement {
  constructor() {
    super(); //call the constructor of the parent class (i.e., HTMLElement)
  }

  connectedCallback() {
    this.innerHTML = `
    <div class="transition duration-500 ease-in-out flex py-3 px-2 hover:bg-blue-400 transform hover:-translate-y-1 hover:scale-110 hover:text-white hover:shadow-none hover:rounded border border-gray-300 shadow-lg">
      <img src="img/logo.jpg" class="h-16 w-12 mr-20 ml-8 mt-10" alt="Image">
      <div class="w-3/5 mr-0">
        <h2 class="text-gray-800 font-bold">Buzz</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore et excepturi autem iure molestias doloribus ipsa praesentium.</p>
      </div>
    </div>
    `;
  }
}

customElements.define('card-component', Card); //domstring when adding to page, component class